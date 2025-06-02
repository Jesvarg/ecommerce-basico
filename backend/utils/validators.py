import re
from config.settings import Config
from typing import Optional

# --- Validaciones básicas reutilizables ---
def validate_non_empty_string(value, field_name, min_length=1, max_length=255):
    if not isinstance(value, str) or not (min_length <= len(value.strip()) <= max_length):
        raise ValueError(f"{field_name} debe tener entre {min_length} y {max_length} caracteres")


def validate_positive_number(value, field_name, allow_zero=False):
    if value is None or (value < 0 or (not allow_zero and value == 0)):
        raise ValueError(f"{field_name} debe ser mayor {'o igual a' if allow_zero else 'que'} 0")


def validate_email_format(email: str):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Formato de email inválido")


def validate_status(value, allowed_statuses):
    if value not in allowed_statuses:
        raise ValueError(f"Estado inválido. Debe ser uno de: {', '.join(allowed_statuses)}")


def is_valid_image_url(url: Optional[str]) -> bool:
    if not url:
        return False
    return (url.startswith(("http://", "https://", "/static/")) and url.lower().endswith(('.jpg', '.jpeg', '.png', 'webp', 'gif')))



# --- Validaciones específicas ---
def is_valid_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def is_strong_password(password: str) -> bool:
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"\d", password) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )


# --- Validaciones de datos de producto y orden ---
def validate_product_data(data: dict):
    required_fields = ['name', 'price', 'stock', 'category_id']
    if data['price'] > 10000:
        raise ValueError("El límite de precio es de 10000")
    if data['stock'] < 1 or data['stock'] > 10000:
        raise ValueError("El stock no puede exceder mas de 10000 unidades")
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Falta el: '{field}' ")

    validate_non_empty_string(data['name'], 'Nombre del producto', min_length=2, max_length=150)
    validate_positive_number(data['price'], 'Precio')
    
    if not isinstance(data['stock'], int) or data['stock'] < 0:
        raise ValueError("El stock debe ser un número entero no negativo")

    if 'weight' in data and data['weight'] is not None:
        validate_positive_number(data['weight'], 'Peso')

    if 'image_url' in data and data['image_url']:
        if not is_valid_image_url(data['image_url']):
            raise ValueError("La URL o archivo de imagen es inválido")


def validate_payment_method(method: str):
    if method.lower() not in Config.PAYMENT_METHODS:
        raise ValueError(f"Método de pago no soportado, Opciones: {', '.join(Config.PAYMENT_METHODS)}")

def validate_order_items(items_data: list[dict]):
    if not isinstance(items_data, list) or not items_data:
        raise ValueError("La orden debe tener al menos un ítem")

    for item in items_data:
        if 'product_id' not in item:
            raise ValueError("Falta 'product_id' en uno de los productos")
        validate_positive_number(item.get('quantity', -1), 'Cantidad')
        validate_positive_number(item.get('price_at_purchase', -1), 'Precio de compra')
        if 'subtotal' in item:
            validate_positive_number(item['subtotal'], 'Subtotal')

def validate_order_payment(data: dict):
    validate_positive_number(data.get("amount", -1), 'Monto', allow_zero=True)
    validate_positive_number(data.get("total", -1), 'Total', allow_zero=True)
    validate_non_empty_string(data.get("transaction_id", ""), 'ID de transacción', min_length=5)


def validate_order_data(data: dict):
    errors = {}
    
    # Validar campos requeridos
    required_fields = ['user_id', 'total', 'shipping_address', 'payment_method', 'items']
    for field in required_fields:
        if field not in data:
            errors[field] = "Campo requerido"
    
    # Validar tipos y formatos
    if 'user_id' in data and (not isinstance(data['user_id'], int) or data['user_id'] <= 0):
        errors['user_id'] = "Usuario inválido"
    
    if 'total' in data and data['total'] <= 0:
        errors['total'] = "El total debe ser positivo"

    if 'shipping_address' in data:
        if not isinstance(data['shipping_address'], str) or len(data['shipping_address']) < 10:
            errors['shipping_address'] = "La dirección de envío debe ser una cadena de al menos 10 caracteres"
        # Validar que la dirección contenga al menos un número
        elif not any(char.isdigit() for char in data['shipping_address']):
            errors['shipping_address'] = "La dirección de envío debe contener al menos 1 número"
    
    if errors:
        raise ValueError({"errors": errors, "message": "Error de validación en la orden"})

    validate_positive_number(data['total'], 'Total')
    validate_non_empty_string(data['payment_method'], 'Método de pago')
    validate_payment_method(data['payment_method'])

    validate_order_items(data['items'])
