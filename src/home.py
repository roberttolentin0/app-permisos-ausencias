import os
import traceback
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from src.services.EmployeeService import EmployeeService
from src.services.PermissionService import PermissionService
from src.utils.Logger import Logger
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint('home', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    print('go index home')
    return render_template('index.html')

@bp.route('/login_view')
def view_login():
    print('Login permiso', request)
    return render_template('login.html')

@bp.route('/login', methods=['POST'])
def login():
    print('Login permiso', request)
    print('Crear permiso', request.form)
    password = request.form['password']
    if password == os.getenv('PASSWORD_ADMIN'):
        print('go index home')
        # return render_template('index.html')
        return jsonify({ 'message': 'Empleado no encontrado' }), 200
    else:
        return jsonify({ 'message': 'Datos incorrectos' }), 404


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
            if dni in ['77043715', '74083687']: # Antonella and Danne
                employee['user_mode'] = 'admin'
            data_response['employee'] = employee
        else:
            return jsonify({ 'message': 'Empleado no encontrado' }), 404
        # if len(permission) != 0:
        data_response['permission'] = permission
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
    print('data_response', data_response)
    return jsonify({'message': 'success', 'data': data_response}), 200