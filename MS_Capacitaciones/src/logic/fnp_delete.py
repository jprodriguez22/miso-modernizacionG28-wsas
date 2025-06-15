import logging
import traceback
from sqlalchemy import MetaData, Table

from src.constants.servers import SF_SERVER
from src.data.sql_engine import Handler


class FNPDelete:
    def __init__(self, id_fnp, body = None):
        self.id = id_fnp
        self.body = body

    def start_engine(self):
        engine = Handler().start_engine(SF_SERVER)
        
        # Start sqlalchemy handling
        meta = MetaData()
        fnp_table = Table("FNP", meta, schema="dbo", autoload_with=engine)
        return engine, fnp_table

    def execute(self):
        if not self.body:
            return {
                "response": {
                    "message": "No se ha introducido el correo de quien ejecutó la acción"
                },
                "status_code": 403,
            }
            
        submitted_by = self.body['SubmittedBy']    
        
        engine, fnp_table = self.start_engine()

        stmt = fnp_table.delete().where(fnp_table.c.IDFNP == self.id)

        try:
            with engine.connect() as conn:
                conn.execute(stmt)
                conn.commit()

            return {
                "response": {
                    "event": "DELETE FNP",
                    "ID": self.id,
                    "SubmittedBy": submitted_by
                },
                "status_code": 200,
            }

        except Exception as e:
            tb = traceback.format_exc()
            logging.error(f'Se ha detectado el siguiente problema: {tb}', exc_info=True)
            return {
                "response": {
                    "event": "DELETE FNP EXCEPTION",
                    "msg": f"Ha ocurrido un error durante la eliminación de una FNP {self.id}: {tb}",
                },
                "status_code": 500,
            }
