import locale
from flask import Flask
# Routes
from .routes import PermissionRoutes
from src import home

# Crear aplicación de flask
app = Flask(__name__)

def init_app(config):
    app.config.from_object(config)

    locale.setlocale(locale.LC_ALL, 'es_ES')

    # Registrar vistas | Blueprints
    app.register_blueprint(home.bp, url_prefix='/')
    app.register_blueprint(PermissionRoutes.bp, url_prefix='/permisos')

    return app