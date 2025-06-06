from utils.validators import validate_order_items
from database import db

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    order = db.relationship('Order', back_populates='order_items')
    product = db.relationship('Product')

    def __init__(self, **kwargs):
        validate_order_items([kwargs])

        if 'subtotal' not in kwargs and 'price_at_purchase' in kwargs and 'quantity' in kwargs:
            kwargs['subtotal'] = kwargs['price_at_purchase'] * kwargs['quantity']

        super().__init__(**kwargs)
    
    def __repr__(self):
        return f'<OrderItem Order:{self.order_id} Product:{self.product_id} Qty:{self.quantity}>'