from flask import Flask
from models import __all__  # Importas los modelos para que SQLAlchemy los registre
from database import db_handler

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.settings.Config')

    db_handler.init_app(app)

    with app.app_context():
        db_handler.create_tables()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

