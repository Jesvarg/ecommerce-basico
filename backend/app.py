from flask import Flask
from config.settings import Config
from database import db, init_app
from api.routes import all_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar base de datos y migraciones
    init_app(app)

    # Registrar blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)