from . import db
from flask import current_app

def create_tables():
    # Crea todas las tablas definidas en los modelos
    db.create_all()

def drop_tables():
    # Borra todas las tablas, útil en desarrollo
    db.drop_all()

def init_app(app):
    db.init_app(app)
