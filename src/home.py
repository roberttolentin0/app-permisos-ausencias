from flask import Blueprint, render_template, request

bp = Blueprint('home', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    print('go index home')
    return render_template('index.html')

@bp.route("/name/<string:dni>")
def get_name(dni):
    return {
        "dni": dni,
        "name": 'Robert Carlos Tolentino Mendoza'
    }