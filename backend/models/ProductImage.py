from utils.validators import is_valid_image_url, validate_positive_number
from database import db

class ProductImage(db.Model):
    __tablename__ = 'product_images'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        if not is_valid_image_url(kwargs.get("url")):
            raise ValueError("La URL o nombre de archivo de imagen es inválido")
        validate_positive_number(kwargs.get('product_id'), 'ID de producto')
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<Image for Product {self.product_id}>'
