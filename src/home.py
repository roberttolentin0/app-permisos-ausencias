import traceback
from flask import Blueprint, render_template, request, jsonify
from src.services.EmployeeService import EmployeeService
from src.services.PermissionService import PermissionService
from src.utils.Logger import Logger

bp = Blueprint('home', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    print('go index home')
    return render_template('index.html')

@bp.route("/get_data_by_dni/<string:dni>")
def get_data_by_dni(dni):
    try:
        data_response = {}
        # {
        #     'employee': {'dni': '77043715', 'full_name': 'ANTONELLA HAYDEE LOPEZ JULCA', 'user_mode': 'admin'},
        #     'permission': {'id': 24, 'dni': '77043715', 'end_time': None, 'reason': 'Visita market', 'status': 'ACEPTADO', 'observation': '', 'validator_id': 1}
        # }
        employee = EmployeeService.get_name_employee(dni)
        permission = PermissionService.get_permisssion_by_dni(dni)
        if len(employee) != 0:
            employee['user_mode'] = 'user'
            if dni in ['77043715', '12345678']: # Antonella and Danne
                employee['user_mode'] = 'admin'
            data_response['employee'] = employee
        if len(permission) != 0:
            data_response['permission'] = permission
        else:
            return jsonify({ 'message': 'Empleado no encontrado' }), 404
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
    print('data_response', data_response)
    return jsonify({'message': 'success', 'data': data_response}), 200