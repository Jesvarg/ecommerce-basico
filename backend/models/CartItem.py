from utils.validators import validate_positive_number

from database import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('shopping_carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    cart = db.relationship('ShoppingCart', back_populates='items')
    product = db.relationship('Product')

    def __init__(self, **kwargs):
        validate_positive_number(kwargs.get('quantity'), 'Cantidad')
        validate_positive_number(kwargs.get('product_id'), 'ID de producto')
        validate_positive_number(kwargs.get('cart_id'), 'ID de carrito')
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<CartItem Cart:{self.cart_id} Product:{self.product_id} Qty:{self.quantity}>'