from flask import Flask

def create_app():
    # Crear aplicación de flask
    app = Flask(__name__)

    import locale
    locale.setlocale(locale.LC_ALL, 'es_ES')

    # Registrar vistas
    from app import home
    app.register_blueprint(home.bp)

    return app