import numpy as np
import pandas as pd
from io import BytesIO
from dotenv import dotenv_values
from flask_jsonpify import jsonify
from requests import get
from ..models.loader_microservices import Loader


class LeccionesAprendidas:
    def __init__(self, dominio: str, credentials_sf: dict):
        self.credentials_sf = credentials_sf
        self.dominio = dominio
        self.loader_local = Loader()
        self.stored_procedures = dotenv_values("stored_procedures.env")

    def consultar_caracteristicas_orden(self, orden):
        """
        Permite consultar los diferenciales de producto de una orden ingresada
        como parámetro. Retorna una respuesta en formato JSON

        Parameters:
            orden: str
                Orden de producción de la pieza a consultar
        """
        df_consulta = self.loader_local.descargar_datos(
            f"{self.stored_procedures['QUERYINFOORDEN']} WHERE Orden = {orden}"
        )
        try:
            zfer = df_consulta.loc[0]["ZFER"]
            response = (
                get(f"{self.dominio}/api/prediccion_zfer/consultar/{zfer}").json(),
                200,
            )
        except:  # noqa: E722
            response = {"message": "No se ha encontrado la orden consultada"}, 404
        return response

    def actualizar_lecciones_aprendidas(self):
        """
        Carga todas las lecciones aprendidas existentes a la base de datos del
        microservicio. Importante para reducir la latencia y poder ejecutar las
        funciones de este
        """
        try:
            loader_sf = Loader(credentials=self.credentials_sf)
        except ConnectionError:
            return {
                "message": "No se ha podido establecer una conexión con el servidor remoto"
            }, 500
        df_lecciones_aprendidas = loader_sf.descargar_datos(
            self.stored_procedures["QUERYLECCIONES"]
        )
        self.loader_local.cargar_datos(
            df_lecciones_aprendidas, tabla="lecciones_aprendidas", if_exists="replace"
        )
        return {"message": "Base de datos local actualizada"}, 200

    def extraer_lecciones_aprendidas(
        self, puesto_trabajo: str = None, caracteristicas: list = None, zfer: str = None
    ):
        """
        Consulta que retorna las lecciones aprendidas asociadas a una lista de
        características y un puesto de trabajo específico. Solo es posible consultar
        un puesto de trabajo por la naturaleza de la operación. Devuelve una
        respuesta JSON

        Parameters:
            caracteristicas: list
                Lista de las características consultadas
            puesto_trabajo: str
                Puesto de trabajo de la operación a consultar
        """
        df_lecciones_aprendidas = self.loader_local.descargar_datos(
            self.stored_procedures["QUERYLECCIONESLOCAL"]
        )

        if not puesto_trabajo:
            return {"message": "El puesto de trabajo es obligatorio"}, 400

        df_lecciones_aprendidas = df_lecciones_aprendidas[
            df_lecciones_aprendidas["Puesto"] == puesto_trabajo
        ]

        if caracteristicas:
            df_lecciones_aprendidas = df_lecciones_aprendidas[
                df_lecciones_aprendidas["Diferencial"].isin(caracteristicas)
            ]

        df_lecciones_aprendidas_zfer = df_lecciones_aprendidas[
            df_lecciones_aprendidas["ZFER"] == int(zfer)
        ].copy()
        df_lecciones_aprendidas = df_lecciones_aprendidas[
            df_lecciones_aprendidas["ZFER"].isna()
        ]
        df_lecciones_aprendidas = pd.concat(
            [df_lecciones_aprendidas, df_lecciones_aprendidas_zfer]
        )

        df_lecciones_aprendidas["ZFER"] = df_lecciones_aprendidas["ZFER"].replace(
            np.nan, 0
        )

        df_lecciones_aprendidas["Diferencial"] = df_lecciones_aprendidas[
            "Diferencial"
        ].fillna("")
        
        return jsonify(df_lecciones_aprendidas.to_dict(orient="records"))

    def extraer_imagen_leccion(self, id_leccion=None):
        if not id_leccion:
            return {
                "message": "Debe introducir un ID como query para este endpoint"
            }, 400

        id_leccion = int(id_leccion)

        df_imagen_leccion = self.loader_local.descargar_datos(
            f'{self.stored_procedures["QUERYLECCIONESLOCALIMAGEN"]} WHERE ID = {id_leccion}'
        )
        if df_imagen_leccion.empty:
            return {"message": "Esta lección aprendida no existe"}, 404

        imagen = df_imagen_leccion.loc[0]["Imagen"]
        if not imagen:
            return {
                "message": "Esta lección aprendida no tiene una imagen asociada"
            }, 404
        imagen = BytesIO(imagen)
        return imagen, 200
