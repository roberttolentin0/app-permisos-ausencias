from flask import Blueprint, render_template, request

bp = Blueprint('home', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    print('index')
    return render_template('index.html')