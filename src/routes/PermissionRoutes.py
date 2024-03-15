import traceback

from flask import Blueprint, render_template, request, jsonify, flash

# Logger
from src.utils.Logger import Logger
# Models
from src.models.PermissionModel import Permission
from src.models.EmployeeModel import Employee
# Services
from src.services.PermissionService import PermissionService
from src.services.EmployeeService import EmployeeService

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
            full_name = request.form['full_name']
            print('dni_form', dni)
            permission_date = request.form['fecha']
            start_time = request.form['hora_salida']
            end_time = request.form['hora_retorno']
            reason = request.form['motivo']
            status = 'PENDIENTE'
            observation = ''
            validator_id = '1' # request.json['validator_id']
            # Create Employee
            try:
                employee = Employee(dni, full_name)
                affected_rows = EmployeeService.create_employee(employee=employee)
            except Exception as e:
                Logger.add_to_log("error", str(e))
                Logger.add_to_log("error", traceback.format_exc())
            # Create permission
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
        print('Actualizar permiso', request)
        data = request.json
        # print('data', data)
        id = data['id']
        action = data['action']
        affected_rows = None

        if action == 'aceptar':
            affected_rows = PermissionService.update_status_permission(id=id, status='ACEPTADO')
        elif action == 'rechazar':
            rejection_reason = data['rejection_reason']
            affected_rows = PermissionService.update_status_permission(id=id, status='RECHAZADO', observation=rejection_reason)
        elif action == 'extender':
            affected_rows = PermissionService.update_status_permission(id=id, status='EXTENDIDO')
            print('Extender Permiso')

        if affected_rows == 1:
            return jsonify({'message': 'success'}), 200
        else:
            return jsonify({'message': "Error on update"}), 500
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())

# @bp.route('/accept_permission', methods=['POST'])
# def accept_permission():
#     try:
#         print('Actualizar permiso, estado aceptado')
#         return jsonify({'message': 'success', 'data': {}}), 200
#     except Exception as e:
#         Logger.add_to_log("error", str(e))
#         Logger.add_to_log("error", traceback.format_exc())