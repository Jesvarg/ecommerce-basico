from werkzeug.security import generate_password_hash, check_password_hash
from utils.validators import is_valid_email, is_strong_password
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

    orders = db.relationship('Order', back_populates='user', lazy=True)
    cart = db.relationship('ShoppingCart', back_populates='user', uselist=False)

    def __init__(self, **kwargs):
        self.validate_first_name(kwargs.get('first_name'))
        self.validate_last_name(kwargs.get('last_name'))
        self.validate_email(kwargs.get('email'))

        password = kwargs.pop('password', None)
        if  password:
            self.set_password(password)
        elif 'password_hash' in kwargs:
            self.validate_password(kwargs['password_hash'])
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
        if not is_valid_email(email):
            raise ValueError("Formato de email inválido")

    def validate_password(self, password):
        if not is_strong_password(password):
            raise ValueError("Contraseña débil: mínimo 8 caracteres, mayúscula, minúscula, número y símbolo")
        
    def set_password(self, password):
        self.validate_password(password)
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'