from database import db

class ShoppingCart(db.Model):
    __tablename__ = 'shopping_carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    user = db.relationship('User', backref=db.backref('cart', uselist=False))

    def __repr__(self):
        return f'<Cart User {self.user_id}>'