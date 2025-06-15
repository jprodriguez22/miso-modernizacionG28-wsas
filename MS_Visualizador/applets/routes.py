"""This file contains all the routes that are relevant to the different areas that are relevant in production. They depend entirely on the state.
It must be imported in the main app as a blueprint later"""

from flask import Blueprint, request, send_file
from . import handler

routing = Blueprint("routes", __name__, template_folder="templates")


@routing.get("/api/visualizador")
def preload_database():
    response = handler.visualizador.main("actualizar_planos")
    return response


@routing.get("/api/visualizador/<orden>")
def cargar_orden(orden):
    response = handler.visualizador.main("consultar_informacion_orden", orden=orden)
    return response


@routing.get("/api/visualizador/<orden>/plano")
def cargar_plano(orden):
    response, status = handler.visualizador.main("consultar_plano", orden=orden)
    if status == 404:
        return response, status
    else:
        return send_file(response, mimetype="image/jpg"), status


@routing.get("/api/visualizador/lecciones/caracteristicas/<orden>")
def cargar_caracteristicas(orden):
    response = handler.visualizador.main("consultar_caracteristicas_orden", orden=orden)
    return response


@routing.get("/api/visualizador/lecciones/actualizar")
def actualizar_lecciones():
    response = handler.visualizador.main("actualizar_lecciones")
    return response


@routing.post("/api/visualizador/lecciones/consultar")
def consultar_lecciones():
    data = request.get_json()
    caracteristicas = data.get("caracteristicas")
    puesto_trabajo = data.get("puesto_trabajo")
    zfer = data.get("zfer")

    response = handler.visualizador.main(
        "consultar_lecciones",
        caracteristicas=caracteristicas,
        puesto_trabajo=puesto_trabajo,
        zfer=zfer,
    )
    return response


@routing.get("/api/visualizador/lecciones/imagen")
def descargar_imagen_leccion():
    id_leccion = request.args.get("id")
    response, status = handler.visualizador.main(
        "imagen_leccion", id_leccion=id_leccion
    )
    if status != 200:
        return response, status
    return send_file(response, mimetype="image/png")


@routing.post("/api/visualizador/reportes")
def cargar_reporte():
    msg = request.get_json()
    response, status = handler.visualizador.main("encolar_reporte", alert_message=msg)
    return response, status
