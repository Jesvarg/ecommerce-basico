from flask import Blueprint, request, jsonify
from utils import is_valid_image_url, is_valid_price, is_valid_stock
from api.products import create_product, get_all_products, get_product_by_id, update_product_stock, update_product_price

product_bp = Blueprint('products', __name__)


@product_bp.route('/products', methods=['GET'])
def list_products():
    products = get_all_products()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "stock": p.stock,
        "category": p.category
    } for p in products]), 200


@product_bp.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    
    required_fields = ['name', 'price', 'stock', 'category']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo '{field}'"}), 400

    if not is_valid_price(data['price']):
        return jsonify({"error": "Debes ingresar un precio válido"}), 400
    
    if not is_valid_stock(data['stock']):
        return jsonify({"error": "El stock no puede ser negativo"}), 400
    
    if not is_valid_image_url(data.get('image_url', '')):
        return jsonify({"error": "La imagen no es válida"}), 400

    product = create_product(
        name=data['name'],
        description=data.get('description'),
        category=data['category'],
        price=data['price'],
        stock=data['stock'],
        weight=data.get('weight'),
        image_url=data.get('image_url')
    )

    return jsonify({"message": "Producto creado", "id": product.id}), 201


@product_bp.route('/products/<int:product_id>/stock', methods=['PUT'])
def update_stock(product_id):
    data = request.get_json()
    if 'stock' not in data:
        return jsonify({"error": "Campo 'stock' requerido"}), 400

    if data['stock'] < 0:
        return jsonify({"error": "El stock no puede ser negativo"}), 400

    try:
        product = update_product_stock(product_id, data['stock'])
        return jsonify({"message": "Stock actualizado", "stock": product.stock})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400