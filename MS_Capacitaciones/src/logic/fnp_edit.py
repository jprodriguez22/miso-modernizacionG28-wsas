import logging
import traceback
from datetime import datetime
from sqlalchemy import MetaData, Table

from src.constants.servers import SF_SERVER
from src.data.sql_engine import Handler


class FNPEdit:
    def __init__(self, id_fnp, body: dict):
        self.id = id_fnp
        self.body = body

    def start_engine(self):
        engine = Handler().start_engine(SF_SERVER)
        
        # Start sqlalchemy handling
        meta = MetaData()
        fnp_table = Table("FNP", meta, schema="dbo", autoload_with=engine)
        return engine, fnp_table

    def check_body(self):
        return any(
            [
                x in self.body
                for x in ["Customer", "SubmittedBy", "Project", "Title", "ZFERList"]
            ]
        )

    def execute(self):
        validations = self.check_body()
        if not validations:
            return {
                "response": "Se ha solicitado una actualización sin ningún campo diligenciado"
            }

        engine, fnp_table = self.start_engine()

        stmt = fnp_table.update().where(fnp_table.c.IDFNP == self.id).values(
            FechaCarga = datetime.now(),
            Version = fnp_table.c.Version + 1,
            Cliente = self.body['Customer'],
            Proyecto = self.body['Project'],
            CargadoPor = self.body['SubmittedBy'],
            Nombre = self.body['Title'],
            ZFER = self.body['ZFERList'],            
        )

        try:
            with engine.connect() as conn:
                conn.execute(stmt)
                conn.commit()

            return {
                "response": {
                    "event": "UPDATE FNP",
                    "ID": self.id,
                    "Cuerpo": self.body,
                },
                "status_code": 200,
            }

        except Exception as e:
            tb = traceback.format_exc()
            logging.error(f'Se ha detectado el siguiente problema: {tb}', exc_info=True)
            return {
                "response": {
                    "event": "UPDATE FNP EXCEPTION",
                    "msg": f"Ha ocurrido un error durante la actualización de un dato en el FNP {self.id}: {tb}",
                },
                "status_code": 500,
            }
