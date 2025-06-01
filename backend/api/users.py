from models import User
from database import db
from werkzeug.security import generate_password_hash
from typing import Optional

def create_user(first_name: str, last_name: str, email: str, password: str, role: str = "user") -> User:
    """Crear un nuevo usuario"""
    if User.query.filter_by(email=email).first():
        raise ValueError("El email ya está registrado")

    hashed_password = generate_password_hash(password)

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=hashed_password,
        role=role
    )

    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_email(email: str) -> Optional[User]:
    """Buscar usuario por email"""
    return User.query.filter_by(email=email).first()


def verify_user_password(email: str, password: str) -> bool:
    """Verifica contraseña de usuario"""
    user = get_user_by_email(email)
    return user is not None and user.check_password(password)


def get_user_by_id(user_id: int) -> Optional[User]:
    """Obtener usuario por ID"""
    return User.query.get(user_id)


def update_user_role(user_id: int, new_role: str) -> User:
    """Actualizar rol de usuario"""
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("El usuario no existe")
    
    user.role = new_role
    db.session.commit()
    return user


def delete_user(user_id: int) -> None:
    """Eliminar usuario"""
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("El usuario no existe")
    
    db.session.delete(user)
    db.session.commit()