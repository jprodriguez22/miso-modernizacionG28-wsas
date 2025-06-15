import datetime as dt
import pandas as pd
from os import getenv

from .loader_microservices import MicroServiceLoader
pd.set_option('future.no_silent_downcasting', True)

class DataHandler:
    def __init__(self):
        self.credentials_calendario = {"DRIVER": getenv('DRIVER'), "USER": getenv('CALUSER'), "PWD": getenv('CALPWD'), "SERVER": getenv('CALSERVER'),  "DB": getenv('CALDB') }
        self.credentials_productivity = {"DRIVER": getenv('DRIVER'), "USER": getenv('PRODUSER'), "PWD": getenv('PRODPWD'), "SERVER": getenv('PRODSERVER'),  "DB": getenv('PRODDB') }
        self.credentials_smartfactory = {"DRIVER": getenv('DRIVER'), "USER": getenv('SFUSER'), "PWD": getenv('SFPWD'), "SERVER": getenv('SFSERVER'),  "DB": getenv('SFDB') }
        
        self.loader_microservice = MicroServiceLoader()
    
    def prepare_dataset(self):
        '''
        This method is in charge of extracting the data from the sources and transforming it. It returns the processed dataset
        '''
        loader_calendario = MicroServiceLoader(self.credentials_calendario)
        loader_productivity = MicroServiceLoader(self.credentials_productivity)
        df_calendario = loader_calendario.descargar_datos(getenv('QUERYCALENDARIO'))
        df_costos_consumo = loader_productivity.descargar_datos(getenv('QUERYCOSTOCONSUMOS'))
        # TODO: Incluir consulta de desperdicios
        
        df_control_costos = pd.merge(df_calendario[~df_calendario['LlegoAlmacen']], df_costos_consumo, on='Orden', how='left')
        df_control_costos = df_control_costos.sort_values(by='RelacionSobrecosto', ascending=False)
        
        df_control_costos.loc[(df_control_costos['Puestodetrabajo'].str.contains('01CORTE|02CNC|03SERIG|04SER_VT|05EMPAL')), 'Bloque'] = 'Bloque Plano'
        df_control_costos.loc[(df_control_costos['Puestodetrabajo'].str.contains('06CURVAD|07RECORT|08S_RUCO|08PULIDO|09IOX_E|09IOX_S|12P_ENSA')), 'Bloque'] = 'Bloque Curvo'
        df_control_costos.loc[(df_control_costos['Puestodetrabajo'].str.contains('14ENSAM|15EMBOL')), 'Bloque'] = 'Bloque Blindado'
        df_control_costos.loc[(df_control_costos['Puestodetrabajo'].str.contains('Planeacion')), 'Bloque'] = 'Planeacion'
        df_control_costos['Bloque'] = df_control_costos['Bloque'].fillna('Calidad')
        
        df_control_costos['FechaRegistro'] = df_control_costos['FechaRegistro'].fillna(dt.datetime(1900, 1, 1))
        df_control_costos['CostoPlan'] = df_control_costos['CostoPlan'].fillna(0)
        df_control_costos['CostoReal'] = df_control_costos['CostoReal'].fillna(0)
        df_control_costos['RelacionSobrecosto'] = df_control_costos['RelacionSobrecosto'].fillna(0)
        df_control_costos['Complex'] = df_control_costos['Complex'].fillna(False)
        df_control_costos = df_control_costos.fillna('')
        df_control_costos['Mercado'] = df_control_costos['Mercado'].str.upper()
        
        df_control_costos = df_control_costos.astype({'FechaRegistro': 'datetime64[ns]'})
        df_control_costos['CostoPlan'] = df_control_costos['CostoPlan'].round(2)
        df_control_costos['CostoReal'] = df_control_costos['CostoReal'].round(2)
        df_control_costos['RelacionSobrecosto'] = df_control_costos['RelacionSobrecosto'].round(2)
        
        return df_control_costos
    
    def update_local_dataset(self, df):
        df = df.drop_duplicates()
        self.loader_microservice.cargar_datos(pd.DataFrame([{'update_time': dt.datetime.now()}]), 'update_time', 'replace')
        self.loader_microservice.cargar_datos(df, 'local_dataset', 'replace')        
    
    def update_remote_dataset(self, df):
        df = df.drop_duplicates()
        loader_smartfactory = MicroServiceLoader(self.credentials_smartfactory)
        loader_smartfactory.ejecutar_query(getenv('QUERYLIMPIARTABLACOSTOS'))
        loader_smartfactory.cargar_datos(df, 'SF_CostoOrdenesActivas', 'append', index=True, index_label='Index')
    
    def load_dataset(self):
        '''
        Loads the dataset either from the cache or by calling the prepare_dataset method, depending on the conditions fulfilled
        '''
        update_time = self.loader_microservice.ultima_modificacion()
        if update_time:          
            update_time = dt.datetime.strptime(update_time, '%Y-%m-%d %H:%M:%S.%f')
            df_control_costos = self.loader_microservice.descargar_datos('SELECT * FROM local_dataset')
        else:
            df_control_costos = self.prepare_dataset()
            df_control_costos = df_control_costos.drop_duplicates()
        return df_control_costos