from flask import Flask

def create_app():
    # Crear aplicación de flask
    app = Flask(__name__)

    import locale
    locale.setlocale(locale.LC_ALL, 'es_ES')

    # Registrar vistas
    from src import home
    from src.routes import PermissionRoutes
    app.register_blueprint(home.bp)
    app.register_blueprint(PermissionRoutes.bp)
    return app