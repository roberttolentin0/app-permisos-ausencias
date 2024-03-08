from flask import Flask
from flask import url_for
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'login'
    else:
        return 'noLogin'


@app.post('/login') # Para metodos POST tbn hay @app.get('/')
def login_post():
    return 'do_the_login'

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))