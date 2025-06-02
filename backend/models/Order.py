from utils.validators import validate_order_data

from database import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    order_date = db.Column(db.DateTime, default=db.func.now())
    shipping_address = db.Column(db.String(255), nullable=False)

    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    order_items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        validate_order_data(kwargs)
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<Order {self.id} - User {self.user_id}>'