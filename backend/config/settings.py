import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno desde .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config:
    # Clave secreta para JWT y sesiones
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev_jwt_secret")

    # Configuración de la base de datos (ejemplo con PostgreSQL)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///db.sqlite3"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuraciones de seguridad
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.getenv("FLASK_ENV") == "production"
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 86400  # 1 día

    # Configuración de CORS
    CORS_HEADERS = "Content-Type"

    # Debug
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1"]

