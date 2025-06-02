from database import db

class ShoppingCart(db.Model):
    __tablename__ = 'shopping_carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    user = db.relationship('User', back_populates='cart', uselist=False)
    items = db.relationship('CartItem', back_populates='cart', cascade='all, delete-orphan', lazy=True)
    
    @property
    def total(self):
        return sum(item.quantity * item.product.price for item in self.items)

    def __repr__(self):
        return f'<Cart User {self.user_id}>'