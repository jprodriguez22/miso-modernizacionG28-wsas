"""This file contains all the routes that are relevant to the different areas that are relevant in production. They depend entirely on the state.
It must be imported in the main app as a blueprint later"""

from flask import Blueprint, request, send_file
from flask_jsonpify import jsonify
from .handler import GestorOrdenes

routing = Blueprint("routes", __name__, template_folder="templates")

@routing.get("/api/produccion/costos")
def load_dataset():
    response = GestorOrdenes.main('load_data')
    response = jsonify(response.to_dict(orient='records'))
    return response

@routing.get("/api/produccion/costos/defectos/<orden>")
def load_details_defect(orden):
    response = GestorOrdenes.main('load_order_details_defect', order=orden)
    if response[1] == 404:
        return response[0], 404
    response = jsonify(response[0].to_dict(orient='records'))
    return response

@routing.get("/api/produccion/costos/origenes/<orden>")
def load_details_origin(orden):
    response = GestorOrdenes.main('load_order_details_origin', order=orden)
    if response[1] == 404:
        return response[0], 404
    response = jsonify(response[0].to_dict(orient='records'))
    return response
