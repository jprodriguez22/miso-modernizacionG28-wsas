import logging
import traceback
from json import dumps
from sqlalchemy import select, MetaData, Table

from src.constants.servers import SF_SERVER
from src.data.sql_engine import Handler

class FNPGetAll:
    def start_engine(self):
        engine = Handler().start_engine(SF_SERVER)
        
        # Start sqlalchemy handling
        meta = MetaData()
        fnp_table = Table("FNP", meta, schema="dbo", autoload_with=engine)
        return engine, fnp_table

    def execute(self):
        try:
            engine, fnp_table = self.start_engine()
            
            stmt = select(fnp_table)
            with engine.connect() as conn:
                result = conn.execute(stmt)
                rows = result.mappings().all()

            response = [dict(row) for row in rows]
            response = dumps(response, default=str)
            
            return {'response': response, 'status_code': 200}
        
        except Exception:
            tb = traceback.format_exc()
            logging.error(f'Se ha detectado el siguiente problema: {tb}', exc_info=True)
            return {'response': {'message': f'Ha ocurrido un error durante la ejecución desde el servidor: {tb}'}, 'status_code': 500}