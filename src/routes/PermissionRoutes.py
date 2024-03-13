import traceback

from flask import Blueprint, render_template, request, jsonify, flash

# Logger
from src.utils.Logger import Logger
# Models
from src.models.PermissionModel import Permission
# Services
from src.services.PermissionService import PermissionService

bp = Blueprint('permission_blueprint', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    try:
        permissions = PermissionService.get_permisssions()
        if (len(permissions) > 0):
             print('go index permisos', permissions)
        else:
            Exception('No hay permisos')
            # return jsonify({'message': "NOTFOUND", 'success': True})
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
    return render_template('table.html')

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

@bp.route('/crear')
def view_create_permission():
    print('Request for add restaurant page received')
    return render_template('create_permission.html')

@bp.route('/crear_permiso', methods=['POST'])
def create_permission():
    print('Crear permiso')
    try:
        if request.method == 'POST':
            # name = request.values.get('restaurant_name')
            dni = request.form['dni']
            print('dni_form', dni)
            dni = request.json['dni']
            print('dni_json:', dni)
            permission_date = request.json['permission_date']
            start_time = request.json['start_time']
            end_time = request.json['end_time']
            reason = request.json['reason']
            status = request.json['status']
            observation = request.json['observation']
            validator_id = '1' # request.json['validator_id']
            return jsonify({'success': True, 'status': 200})
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        flash('Invalid password provided', 'error')

    return render_template('create_permission.html')

@bp.route('/update_permission', methods=['POST'])
def update_permission():
    try:
        print('Actualizar permiso')
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())