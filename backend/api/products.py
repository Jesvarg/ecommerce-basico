from models import Product
from database import db
from typing import Optional

def get_all_products() -> list[Product]:
    return Product.query.all()


def get_product_by_id(product_id: int) -> Optional[Product]:
    return Product.query.get(product_id)


def create_product(name: str, description: str, category: str, price: float, stock: int,
                   weight: float = None, image_url: str = None) -> Product:
    product = Product(
        name=name,
        description=description,
        category=category,
        price=price,
        stock=stock,
        weight=weight,
        image_url=image_url
    )
    db.session.add(product)
    db.session.commit()
    return product


def filter_products_by_category(category: str) -> list[Product]:
    return Product.query.filter_by(category=category).all()


def update_product_stock(product_id: int, new_stock: int) -> Product:
    product = get_product_by_id(product_id)
    if not product:
        raise ValueError("Producto no encontrado")
    
    product.stock = new_stock
    db.session.commit()
    return product


def update_product_price(product_id: int, new_price: float) -> Product:
    product = get_product_by_id(product_id)
    if not product:
        raise ValueError("Producto no encontrado")
    
    product.price = new_price
    db.session.commit()
    return product


def delete_product(product_id: int) -> None:
    product = get_product_by_id(product_id)
    if not product:
        raise ValueError("Producto no encontrado")
    
    db.session.delete(product)
    db.session.commit()