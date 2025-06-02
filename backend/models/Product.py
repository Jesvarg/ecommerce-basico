from utils.validators import validate_product_data
from database import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, index=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    images = db.relationship('ProductImage', back_populates='product', lazy=True, cascade='all, delete-orphan')
    category = db.relationship('Category', back_populates='products')

    def check_stock(self, quantity):
        if quantity > self.stock:
            raise ValueError(f"Stock insuficiente. Disponible: {self.stock}")
        return True
    
    def update_stock(self, quantity, operation='decrease'):
        if operation == 'decrease':
            if quantity > self.stock:
                raise ValueError(f"Stock insuficiente. Disponible: {self.stock}")
            self.stock -= quantity
        else:
            self.stock += quantity
            
    def __init__(self, **kwargs):
        validate_product_data(kwargs)
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<Product {self.name}>'