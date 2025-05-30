from datetime import datetime
from database import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID único autoincremental
    name = db.Column(db.String(150), nullable=False, index=True)  # Índice para búsqueda frecuente
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=False, index=True)  # Índice para búsquedas por categoría
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.name}>'
