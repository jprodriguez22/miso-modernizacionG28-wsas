from datetime import datetime as dt
from dotenv import dotenv_values
import pandas as pd
from flask_jsonpify import jsonify

from ..models.loader_microservices import Loader


class Plano:
    def __init__(self, credentials_sap, credentials_cal):
        self.credentials_cal = credentials_cal
        self.credentials_sap = credentials_sap
        self.loader_ms = Loader()
        self.stored_procedures = dotenv_values("stored_procedures.env")

    def actualizar_planos(self):
        """
        Este método se encarga de descargar los datos origen desde los
        diferentes servidores y los almacena en una base de datos local
        para poder hacer la carga de manera más rápida
        """
        self.loader_cal = Loader(self.credentials_cal)
        self.loader_sap = Loader(self.credentials_sap)
        try:
            df_orden = self.loader_cal.descargar_datos(                
                self.stored_procedures["QUERYCALENDARIO"]
            )
            df_planos = self.loader_sap.descargar_datos(
                self.stored_procedures["QUERYSAPING"]
            )
            df_orden = df_orden.astype({"ZFER": "int64"})
            df = pd.merge(df_orden, df_planos, on="ZFER", how="left")
            df = df.drop_duplicates(subset=["Orden", "ZFER"])
            df["Plano"] = "\\" + df["Plano"]
            df["Actualizado"] = dt.now()
            self.loader_ms.cargar_datos(df, "mapa_planos", if_exists="replace")
            return {"message": "Se ha actualizado correctamente la base de planos"}, 200
        except Exception as e:
            return {"message": f"No se ha podido actualizar la base por el siguiente error {e}"}, 500

    def consultar_plano(self, orden: str):
        """
        Consultar la ruta de un plano en la base de datos del microservicio.
        En caso de que exista, la retorna como un archivo que puede ser leído
        como un blob desde el servicio que haga la solicitud

        Parameters:
            orden: str
                Orden de producción de la pieza a consultar
        """
        if not orden:
            return {"message": "No se ha introducido un valor"}, 400
        if len(orden) < 8:
            return {
                "message": "No se ha introducido una orden válida. Revise la longitud"
            }, 400
        query = f"{self.stored_procedures['QUERYCONSULTARPLANOS']} WHERE Orden = {orden}"
        consulta = self.loader_ms.descargar_datos(query)
        if consulta.empty:
            return {"message": "No se encuentra la orden en calendario"}, 404
        imagen = consulta["Plano"].iloc[0]
        if not imagen:
            return {
                "message": "No se encuentra la imagen del plano asociado a esta orden"
            }, 404
        return imagen, 200

    def consultar_info_orden(self, orden: str):
        """
        Consultar los datos generales asociados a la orden de producción. En caso
        de que existan, los retorna como un objeto JSON

        Parameters:
            orden: str
                Orden de producción de la pieza a consultar
        """
        if not orden:
            return {"message": "No se ha introducido un valor"}, 400
        if len(orden) < 8:
            return {
                "message": "No se ha introducido una orden válida. Revise la longitud"
            }, 404
        query = f"{self.stored_procedures['QUERYINFOORDEN']} WHERE Orden = {orden}"
        consulta = self.loader_ms.descargar_datos(query)
        if consulta.empty:
            return {"message": "No se encuentra la orden en calendario"}, 404
        return jsonify(consulta.to_dict(orient="records")), 200
