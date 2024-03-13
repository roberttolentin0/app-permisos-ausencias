import traceback

from flask import Blueprint, render_template, request, jsonify, flash

# Logger
from src.utils.Logger import Logger
# Models
from src.models.PermissionModel import Permission
# Services
from src.services.PermissionService import PermissionService

bp = Blueprint('permission_blueprint', __name__)

@bp.route('/', methods=['GET'])
def index():
    permissions = []
    try:
        permissions = PermissionService.get_permisssions()
        if (len(permissions) > 0):
             print('go index permisos', permissions)
        else:
            Exception('No hay permisos')
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())

    return render_template('list_permissions.html', permissions = permissions)

@bp.route('/<int:id>', methods=['GET'])
def get_permission(id):
    try:
        permission = PermissionService.get_permisssion(id)
        if permission is not None:
             print('go index permisos', permission)
        else:
            Exception('No hay permisos')
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
    return permission

@bp.route('/crear_permiso', methods=['POST'])
def create_permission():
    print('Crear permiso', request.form)
    try:
        if request.method == 'POST':
            dni = request.form['dni']
            print('dni_form', dni)
            permission_date = request.form['fecha']
            start_time = request.form['hora_salida']
            end_time = request.form['hora_retorno']
            reason = request.form['motivo']
            status = 'PENDIENTE'
            observation = ''
            validator_id = '1' # request.json['validator_id']
            permission = Permission(None, dni, permission_date, start_time, end_time, reason, status, observation, validator_id)
            affected_rows = PermissionService.create_permission(permission=permission)
            if affected_rows == 1:
                return jsonify({'message': 'success', 'data': {'dni': permission.dni}}), 200
            else:
                return jsonify({'message': "Error on insert"}), 500
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': str(e)}), 500

@bp.route('/update_permission', methods=['POST'])
def update_permission():
    try:
        print('Actualizar permiso')
        return jsonify({'message': 'success', 'data': {}}), 200
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())