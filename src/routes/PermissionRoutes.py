import traceback
from flask import Blueprint, render_template, request, jsonify, flash
from datetime import datetime
# Logger
from src.utils.Logger import Logger
# Models
from src.models.PermissionModel import Permission
from src.models.EmployeeModel import Employee
# Services
from src.services.microsoft_teams_service import cron_send_notification_teams
from src.services.EmployeeService import EmployeeService
from src.services.PermissionService import PermissionService
from src.services.PermissionDetailsService import PermissionDetailsService

bp = Blueprint('permission_blueprint', __name__)

@bp.route('/', methods=['GET'])
def index():
    permissions = []
    try:
        permissions = PermissionService.get_permisssions()
        if (len(permissions) > 0):
             print('go index permisos')
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
    return permission.to_json()

@bp.route('get_permission_details/<int:id>', methods=['GET'])
def get_permission_details(id):
    print('get_permission_details', id)
    try:
        permission = PermissionDetailsService.get_details_by_permission_id(id)
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
            return_time = request.form['hora_retorno']
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
            permission = Permission(None, dni, permission_date, start_time, return_time, reason, status, observation, validator_id)
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
            cron_send_notification_teams('INIT')
        elif action == 'rechazar':
            rejection_reason = data['rejection_reason']
            affected_rows = PermissionService.update_status_permission(id=id, status='RECHAZADO', observation=rejection_reason)
        elif action == 'pedir':
            print('Pedir Extensión Permiso')
            new_return_time = data['newTime']
            new_reason = data['newReason']
            # Guardar en permission_details
            affected_rows = PermissionService.extend_return_time_permission(id_permission=id, new_return_time=new_return_time, new_reason=new_reason)
        elif action == 'extender':
            # Cambia el estado a FINALIZADO y crea una nueva solicitud de permiso
            affected_rows = PermissionService.end_time_permission(id=id)
            # obtener este ultimo permiso
            old_permission = PermissionService.get_permisssion(id)
            # Crear uno nuevo con los datos del ultimo permission_details
            new_detail_permission = PermissionDetailsService.get_last_details_by_permission_id(id)
            print('new_detail_permission', new_detail_permission)
            # Create permission
            curr_time = datetime.now().strftime("%H:%M")
            new_return_time = new_detail_permission['return_time']
            new_reason = old_permission.reason # new_detail_permission['reason']
            permission = Permission(None, old_permission.dni, old_permission.permission_date, curr_time, new_return_time, new_reason, 'PENDIENTE', '', 1)
            affected_rows = PermissionService.create_permission(permission=permission)
        elif action == 'eliminar':
            affected_rows = PermissionService.update_status_permission(id=id, status='ELIMINADO')
            print('Eliminar Permiso')
        elif action == 'finalizar':
            affected_rows = PermissionService.end_time_permission(id=id)
            print('Finalizar Permiso')
        if affected_rows == 1:
            return jsonify({'message': 'success'}), 200
        else:
            return jsonify({'message': "Error on update"}), 500
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
