from flask import Blueprint, request, jsonify
from utils import validate_order_items
from api.users import get_user_by_id
from api.orders import create_order, get_orders_by_user, update_order_status, cancel_order, get_order_by_id

order_bp = Blueprint('orders', __name__)

@order_bp.route('/orders', methods=['POST'])
def create_new_order():
    data = request.get_json()
    
    required_fields = ['user_id', 'total', 'shipping_address', 'payment_method', 'items']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo '{field}'"}), 400

    if data['total'] <= 0:
        return jsonify({"error": "El total debe ser mayor a cero"}), 400

    try:
        validate_order_items(data['items'])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    user = get_user_by_id(data['user_id'])

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 400
    try:
        order = create_order(
        user_id=data['user_id'],
        total=data['total'],
        status=data.get('status', 'pending'),
        shipping_address=data['shipping_address'],
        payment_method=data['payment_method'],
        items_data=data['items']
        )
        return jsonify({"message": "Orden creada", "order_id": order.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@order_bp.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    orders = get_orders_by_user(user_id)
    return jsonify([{
        "id": o.id,
        "total": o.total,
        "status": o.status,
        "date": o.order_date.isoformat() if o.order_date else None
    } for o in orders]), 200


@order_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
def change_status(order_id):
    data = request.get_json()
    if 'new_status' not in data:
        return jsonify({"error": "Campo 'new_status' requerido"}), 400

    try:
        order = update_order_status(order_id, data['new_status'])
        return jsonify({"message": "Estado actualizado", "status": order.status})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@order_bp.route('/orders/<int:order_id>/cancel', methods=['POST'])
def cancel_order_route(order_id):
    order = get_order_by_id(order_id)
    if not order:
        return jsonify({"error": "Orden no encontrada"}), 404
    
    if order.status == "cancelled":
        return jsonify({"error": "La orden ya fue cancelada"}), 400
    try:
        cancel_order(order_id)
        return jsonify({"message": "Orden cancelada"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400