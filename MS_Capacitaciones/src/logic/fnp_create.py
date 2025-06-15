import logging
import traceback
from datetime import datetime
from re import match
from sqlalchemy import insert, MetaData, Table

from src.constants.servers import SF_SERVER
from src.data.sql_engine import Handler

class FNPCreate:
    def __init__(self, body:dict):
        self.body = body

    def start_engine(self):
        engine = Handler().start_engine(SF_SERVER)
        # Start sqlalchemy handling
        meta = MetaData()
        fnp_table = Table("FNP", meta, schema="dbo", autoload_with=engine)
        return engine, fnp_table

    def check_required_fields(self):
        if not self.body["Customer"] or not self.body["Project"] or not self.body["Title"] or not self.body["ZFERList"]:
            return False
        return True

    def check_inputs_not_empty(self):
        if (
            not self.body["Customer"].strip()
            or not self.body["Project"].strip()
            or not self.body["Title"].strip()
        ):
            return False
        return True

    def check_zfers_integrity(self):
        numeric_only_regex = r"^\d+$"
        for zfer in self.body["zfers"]:
            if not match(numeric_only_regex, zfer):
                return False
        return True

    def validations(self):
        if self.check_required_fields():
            return {
                "response": {
                    "message": "No se han introducido todos los parámetros requeridos"
                },
                "status_code": 400,
            }

        if self.check_inputs_not_empty():
            return {
                "response": {"message": "Se ha introducido un campo con solo espacios"},
                "status_code": 400,
            }

        if self.check_zfers_integrity():
            return {
                "response": {
                    "message": "Todos los ZFER deben incluir únicamente números"
                },
                "status_code": 400,
            }
        return True

    def execute(self):
        validations = self.validations()
        if not validations:
            return validations
        
        customer = self.body["Customer"]
        submitted_by = self.body["SubmittedBy"]
        project = self.body["Project"]
        title = self.body["Title"]
        zfers = self.body["ZFERList"]

        engine, fnp_table = self.start_engine()
        list_zfer = zfers.strip()

        stmt = insert(fnp_table).values(
            FechaCarga=datetime.now(),
            Version=1,
            Nombre=title,
            Proyecto=project,
            ZFER=list_zfer,
            Cliente=customer,
            CargadoPor=submitted_by,
        )
        try:
            with engine.connect() as conn:
                conn.execute(stmt)
                conn.commit()
                
            return {
                "response": {
                    "event": "INSERT FNP",
                    "Título": title,
                    "Proyecto": project,
                    "ZFER": list_zfer,
                    "Cliente": customer,
                    "Usuario": submitted_by,
                },
                "status_code": 200,
            }
        
        except Exception as e:
            tb = traceback.format_exc()
            logging.error(f'Se ha detectado el siguiente problema: {tb}', exc_info=True)
            return {
                "response": {
                    "event": "INSERT FNP EXCEPTION",
                    "msg": f"Ha ocurrido un error durante la inserción de un dato: {tb}"
                },
                "status_code": 500
            }