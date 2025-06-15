import logging
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

class Handler:
    def __init__(self, credentials: dict = None):
        self.engine = self.start_engine(credentials)
    
    def start_engine(self, credentials=None):
        try:
            if credentials:
                connection_url = URL.create('mssql+pyodbc', username=credentials['USER'], password=credentials['PWD'],
                                    host=credentials['SERVER'], database=credentials['DB'], port=1433,
                                    query={'driver': credentials['DRIVER'], 'TrustServerCertificate': 'yes',
                                           'TDS_Version':'8.0'})
                return create_engine(connection_url)
            return create_engine('sqlite:///src/data/service_dataset.db')
        except Exception as e:
            logging.error(f'Se ha detectado el siguiente problema: {e}', exc_info=True)