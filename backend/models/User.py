from werkzeug.security import generate_password_hash, check_password_hash
from database import db
import re

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index = True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=True, default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, **kwargs):
        self.validate_first_name(kwargs.get('first_name'))
        self.validate_last_name(kwargs.get('last_name'))
        self.validate_email(kwargs.get('email'))
        self.validate_password(kwargs.get('password_hash'))
        super().__init__(**kwargs)

    # === Métodos de validación ===
    @staticmethod
    def validate_first_name(first_name):
        if not 2 <= len(first_name) <= 30:
            raise ValueError("El nombre debe tener entre 2-30 caracteres")
        
    @staticmethod
    def validate_last_name(last_name):
        if not 2 <= len(last_name) <= 50:
            raise ValueError("El nombre debe tener entre 2-50 caracteres")

    @staticmethod
    def validate_email(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Formato de email inválido")

    def validate_password(self, password):
        if len(password) < 8:
            raise ValueError("La contraseña debe tener mínimo 8 caracteres")
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'
