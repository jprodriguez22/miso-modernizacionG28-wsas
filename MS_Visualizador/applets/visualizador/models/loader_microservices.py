# -*- coding: utf-8 -*-
"""
Esta clase es una interfaz hacia la base de datos de WSAS y contiene
todos los métodos para cargar la información necesaria para el funcionamiento 
del sistema
"""
import logging
import pandas as pd
import sqlalchemy
import warnings
from sqlalchemy import text, delete, update, Table
from sqlalchemy.engine import URL

logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(asctime)s [%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

warnings.filterwarnings("ignore", message=".*pandas only supports SQLAlchemy connectable.*")

class Loader:
    def __init__(self, credentials: dict = None):
        if not credentials:
            parametros_conexion = self.inicializar_conexion()
        else:
            parametros_conexion = self.inicializar_conexion(credentials=credentials)
        self.engine = parametros_conexion[0]
        self.connection = parametros_conexion[1]
        self.meta = parametros_conexion[2]
    
    def inicializar_conexion(self, credentials=None):
        try:
            if credentials:
                connection_url = URL.create("mssql+pyodbc", username=credentials['USER'], password=credentials['PWD'],
                                    host=credentials['SERVER'], database=credentials['DB'], port=1433,
                                    query={"driver": credentials['DRIVER'], "TrustServerCertificate": "yes",
                                           "TDS_Version":'8.0'})                
                engine = sqlalchemy.create_engine(connection_url)
            else:
                engine = sqlalchemy.create_engine("sqlite:///applets/visualizador/service_dataset.db")
            connection = engine.connect()
            meta = sqlalchemy.MetaData()        
            return (engine, connection, meta)
        except Exception as e:
            logging.error(f'Se ha detectado el siguiente problema: {e}', exc_info=True)
    
    def descargar_datos(self, query):
        '''
        Carga la información almacenada en la base de datos a partir de un
        query que se introduce como argumento

        Returns
        -------
        pd.DataFrame

        '''
        try:
            with self.engine.connect() as conn:
                df = pd.read_sql(query, conn.connection)
            return df
        except Exception as e:
            logging.error(f'Se ha detectado el siguiente problema: {e}', exc_info=True)
    
    def cargar_datos(self, df: pd.DataFrame, tabla: str, if_exists: str = 'append'):
        """
        Carga los datos al servidor, a la tabla especificada

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame con la información a cargar.
            
        tabla: str
            Nombre de la tabla a la que se cargará la información.
        
        replace: str
            Modo de resolución de conflictos para el cargue de datos. 'append', 'replace'
            'fail'. Por defecto es 'append'.
        """
        try:
            with self.engine.connect() as conn:
                df.to_sql(tabla, conn.connection, index=False, if_exists=if_exists)
        except Exception as e:
            logging.error(f'Se ha detectado el siguiente problema: {e}', exc_info=True)
        
    def borrar_data(self, fecha_limite:str, table_name:str):
        '''
        Borra los datos almacenados que sean menores a una fecha límite inicial

        Parameters
        ----------
        fecha_limite : datetime64
            Fecha en la cuál todo lo que se encuentre atrás de esta se borra.
        
        tabla : str
            Nombre de la tabla en el servidor
        '''
        try:
            tabla = Table(table_name, self.meta, autoload_with=self.engine)
            stmt = delete(tabla).where(tabla.c.Timestampseconds < fecha_limite)
            self.connection.execute(stmt)
        except Exception as e:
            logging.error(f'Se ha detectado el siguiente problema: {e}', exc_info=True)
        
    def ultima_modificacion(self, tabla):
        '''
        Este método retorna la fecha y hora de la última modificación de la base de datos

        Returns
        -------
        fecha: Fecha en formato de texto

        '''
        try:
            stmt = text(f'SELECT MAX(Actualizado) from {tabla}')
            fecha = self.connection.execute(stmt).first()[0]
            return fecha
        except Exception as e:
            logging.error(f'Se ha detectado el siguiente problema: {e}', exc_info=True)
    
        
        
