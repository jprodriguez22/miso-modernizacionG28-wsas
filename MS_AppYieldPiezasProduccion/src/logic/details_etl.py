import datetime as dt
import pandas as pd
from os import getenv

from .loader_microservices import MicroServiceLoader
pd.set_option('future.no_silent_downcasting', True)

class DetailsHandler:
    def __init__(self):
        self.credentials_comercial = {"DRIVER": getenv('DRIVER'), "USER": getenv('COMUSER'), "PWD": getenv('COMPWD'), "SERVER": getenv('COMSERVER'),  "DB": getenv('COMDB') }
        self.loader_microservice = MicroServiceLoader()
    
    def prepare_dataset(self):
        '''
        This method is in charge of extracting the data from the sources and transforming it. It returns the processed dataset
        '''
        loader_comercial = MicroServiceLoader(self.credentials_comercial)
        df_rejections = loader_comercial.descargar_datos(getenv('QUERYCOSTORECHAZOS'))
        df_rejections['Defecto'] = df_rejections['Defecto'].str.capitalize()  
        return df_rejections
    
    def update_local_dataset(self, df):
        '''
        Updates the time and the data in the local database to have control of the update routine
        '''
        df = df.drop_duplicates()
        self.loader_microservice.cargar_datos(pd.DataFrame([{'update_time': dt.datetime.now()}]), 'details_update_time', 'replace')
        self.loader_microservice.cargar_datos(df, 'details_local_dataset', 'replace')        
    
    def load_dataset(self):
        '''
        Loads the dataset either from the cache or by calling the prepare_dataset method, depending on the conditions fulfilled
        '''
        update_time = self.loader_microservice.ultima_modificacion(table='details_update_time')
        if update_time:          
            update_time = dt.datetime.strptime(update_time, '%Y-%m-%d %H:%M:%S.%f')
            df_rejections = self.loader_microservice.descargar_datos('SELECT * FROM details_local_dataset')
        else:
            df_rejections = self.prepare_dataset()
            self.update_local_dataset(df_rejections)
        df_rejections = df_rejections.drop_duplicates()
        return df_rejections
    
    def load_order_details_by_defect(self, order):
        '''
        Returns the data of a specific production order specified by the user
        '''
        df_rejections_order = self.load_dataset()
        df_rejections_order = df_rejections_order[df_rejections_order['Orden'] == int(order)]
        if df_rejections_order.empty:
            return {'message': 'No se ha encontrado la orden seleccionada'}, 404
        df_rejections_order['Costo'] = df_rejections_order['Costo'].fillna(0)
        df_rejections_order['Porcentaje'] = df_rejections_order['Porcentaje'].fillna(0)
        df_rejections_order = df_rejections_order.fillna('')
        
        df_rejections_order_count = df_rejections_order[['Orden', 'Defecto', 'KeyModel']].groupby(['Orden', 'Defecto']).count()
        df_rejections_order_count = df_rejections_order_count.reset_index().rename({'KeyModel': 'Cantidad'}, axis=1)
        
        df_rejections_order_sum = df_rejections_order[['Orden', 'Defecto', 'Costo', 'Porcentaje']].groupby(['Orden', 'Defecto']).sum()
        
        df_rejections_order_group = pd.merge(df_rejections_order_count, df_rejections_order_sum, on=['Orden', 'Defecto'], how='inner')
        
        return df_rejections_order_group, 200
    
    def load_order_details_by_origin(self, order):
        '''
        Returns the data of a specific production order specified by the user
        '''
        df_rejections_order = self.load_dataset()
        df_rejections_order = df_rejections_order[df_rejections_order['Orden'] == int(order)]
        if df_rejections_order.empty:
            return {'message': 'No se ha encontrado la orden seleccionada'}, 404
        df_rejections_order['Costo'] = df_rejections_order['Costo'].fillna(0)
        df_rejections_order['Porcentaje'] = df_rejections_order['Porcentaje'].fillna(0)
        df_rejections_order = df_rejections_order.fillna('')
        
        df_rejections_order_count = df_rejections_order[['Orden', 'Origen', 'KeyModel']].groupby(['Orden', 'Origen']).count()
        df_rejections_order_count = df_rejections_order_count.reset_index().rename({'KeyModel': 'Cantidad'}, axis=1)
        
        df_rejections_order_sum = df_rejections_order[['Orden', 'Origen', 'Costo', 'Porcentaje']].groupby(['Orden', 'Origen']).sum()
        
        df_rejections_order_group = pd.merge(df_rejections_order_count, df_rejections_order_sum, on=['Orden', 'Origen'], how='inner')
        
        return df_rejections_order_group, 200