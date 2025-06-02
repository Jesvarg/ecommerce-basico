from utils.validators import validate_non_empty_string
from database import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)

    products = db.relationship('Product', back_populates='category', lazy=True)

    @staticmethod
    def normalize_name(name):
        return name.strip().lower()
    
    @classmethod
    def name_exists(cls, name):
        normalized_name = cls.normalize_name(name)
        return cls.query.filter(cls.name.ilike(normalized_name)).first() is not None

    def __init__(self, **kwargs):
        name = kwargs.get('name', '')
        validate_non_empty_string(kwargs.get('name'), 'Nombre de categoría', min_length=1, max_length=30)

        normalized_name = self.normalize_name(name)
        if self.name_exists(normalized_name):
            raise ValueError(f"Ya existe una categoría con el nombre '{name}'")
        
        kwargs['name'] = normalized_name
        super().__init__(**kwargs)


    def __repr__(self):
        return f'<Category {self.name}>'
