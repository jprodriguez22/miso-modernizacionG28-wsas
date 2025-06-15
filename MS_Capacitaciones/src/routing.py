from flask import Blueprint, request
from flask_jsonpify import jsonify

from src.logic.fnp_create import FNPCreate
from src.logic.fnp_edit import FNPEdit
from src.logic.fnp_get_all import FNPGetAll
from src.logic.fnp_delete import FNPDelete

routing = Blueprint("routes", __name__, template_folder="templates")

@routing.get('/api/fnp/health')
def health_check():
    return jsonify({'response': 'El servicio está activo'}), 200

@routing.post('/api/fnp')
def create_fnp():
    body = request.get_json()
    obj = FNPCreate(body)
    response = obj.execute()
    return jsonify(response['response']), response['status_code']

@routing.get('/api/fnp')
def get_all_fnp():
    obj = FNPGetAll()
    response = obj.execute()
    return jsonify(response['response']), response['status_code']

@routing.patch('/api/fnp/<id>')
def update_fnp(id):
    body = request.get_json()
    obj = FNPEdit(id, body)
    response = obj.execute()
    return jsonify(response['response']), response['status_code']

@routing.delete('/api/fnp/<id>')
def delete_fnp(id):
    body = request.get_json()
    obj = FNPDelete(id, body=body)
    response = obj.execute()
    return jsonify(response['response']), response['status_code']