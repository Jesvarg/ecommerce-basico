# utils/validation.py
import re
from typing import Optional

def is_valid_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def is_strong_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password): 
        return False
    if not re.search(r"[a-z]", password): 
        return False
    if not re.search(r"\d", password):   
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  
        return False
    return True

def is_valid_stock(stock: int) -> bool:
    return stock >= 0

def is_valid_price(price: float) -> bool:
    return price > 0

def is_valid_image_url(url: Optional[str]) -> bool:
    if not url:
        return True
    return url.startswith("http") and url.endswith((".jpg", ".png", ".jpeg"))


def validate_order_items(items_data: list[dict]):
    for item in items_data:
        if 'product_id' not in item:
            raise ValueError("Falta 'product_id' en uno de los productos")
        if 'quantity' not in item or item['quantity'] <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        if 'price_at_purchase' not in item or item['price_at_purchase'] <= 0:
            raise ValueError("Precio inválido")
        if 'subtotal' in item and item['subtotal'] <= 0:
            raise ValueError("Subtotal inválido")


def validate_product_data(data: dict):
    required_fields = ['name', 'price', 'stock', 'category']
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Falta campo requerido: '{field}'")
    
    if not isinstance(data['price'], (int, float)) or data['price'] <= 0:
        raise ValueError("El precio debe ser un número positivo")

    if not isinstance(data['stock'], int) or data['stock'] < 0:
        raise ValueError("El stock debe ser un número entero no negativo")

    if 'weight' in data and (not isinstance(data['weight'], (int, float)) or data['weight'] <= 0):
        raise ValueError("El peso debe ser un número positivo")

    if 'image_url' in data and not is_valid_image_url(data['image_url']):
        raise ValueError("La URL de imagen es inválida")


def validate_order_data(data: dict):
    required_fields = ['user_id', 'total', 'shipping_address', 'payment_method', 'items']
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Falta campo requerido: '{field}'")

    if not isinstance(data['user_id'], int) or data['user_id'] <= 0:
        raise ValueError("ID de usuario inválido")

    if not isinstance(data['total'], (int, float)) or data['total'] <= 0:
        raise ValueError("El total debe ser un número positiva")

    if not isinstance(data['shipping_address'], str) or len(data['shipping_address']) < 5:
        raise ValueError("Dirección de envío inválida")

    if not isinstance(data['payment_method'], str) or len(data['payment_method']) < 4:
        raise ValueError("Método de pago inválido")

    if not isinstance(data['items'], list) or len(data['items']) == 0:
        raise ValueError("La orden debe tener al menos un ítem")
    
    validate_order_items(data['items'])