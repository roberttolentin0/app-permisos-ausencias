import traceback
from flask import Blueprint, render_template, request, jsonify
from src.services.EmployeeService import EmployeeService
from src.utils.Logger import Logger

bp = Blueprint('home', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    print('go index home')
    return render_template('index.html')

@bp.route("/name/<string:dni>")
def get_name(dni):
    try:
        employee = EmployeeService.get_name_employee(dni)
        if len(employee) != 0:
             print('Empleado', employee)
        else:
            return jsonify({ 'message': 'Empleado no encontrado' }), 404
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
    return jsonify({'message': 'success', 'data': employee}), 200