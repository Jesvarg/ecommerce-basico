from utils.validators import validate_order_payment, validate_status
from database import db

class OrderPayment(db.Model):
    __tablename__ = 'order_payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    paid_at = db.Column(db.DateTime, default=db.func.now())

    order = db.relationship('Order', back_populates='transaction')

    def __init__(self, **kwargs):
        validate_order_payment(kwargs)
        validate_status(kwargs.get('status'), ['pending', 'paid', 'cancelled'])
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<OrderPayment {self.transaction_id} for Order {self.order_id}>'
