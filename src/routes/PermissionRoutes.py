import traceback

from flask import Blueprint, render_template, request

# Logger
from src.utils.Logger import Logger
# Services
from src.services.PermissionService import PermissionService

bp = Blueprint('permission_blueprint', __name__)

@bp.route('/permisos', methods=['GET', 'POST'])
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
    print('go index permisos', permissions)
    return render_template('index.html')