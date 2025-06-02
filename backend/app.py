from flask import Flask
from config.settings import Config
from database import db, init_app
import models
#from api.routes import all_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar base de datos y migraciones
    init_app(app)

    with app.app_context():
        db.create_all()

    # Registrar blueprints
    """ for bp in all_blueprints:
        app.register_blueprint(bp) """

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)