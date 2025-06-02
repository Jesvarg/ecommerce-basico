from flask import Blueprint, request, jsonify
from utils import is_valid_email, is_strong_password
from api.users import create_user, get_user_by_email, verify_user_password

user_bp = Blueprint('users', __name__)


@user_bp.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()
    
    required_fields = ['first_name', 'last_name', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo '{field}'"}), 400
    try:
        user = create_user(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password']
        )
        return jsonify({"message": "Usuario creado", "id": user.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    
    if 'email' not in data or 'password' not in data:
        return jsonify({"error": "Faltan credenciales"}), 400

    if not verify_user_password(data['email'], data['password']):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    user = get_user_by_email(data['email'])
    return jsonify({
        "message": "Login exitoso",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    }), 200