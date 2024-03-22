from flask import Flask
from flask_cors import CORS
from config import config
from src import init_app

configuration = config['development']
app = init_app(configuration)
CORS(app)  # Agregar esta línea para habilitar CORS en tu aplicación

if __name__ == '__main__':
    app.run()