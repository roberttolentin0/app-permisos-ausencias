from flask import Blueprint, render_template, request

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    return render_template('create_permission.html')

@bp.route("/name/<string:dni>")
def get_name(dni):
    return {
        "dni": dni,
        "name": 'Robert Carlos Tolentino Mendoza'
    }