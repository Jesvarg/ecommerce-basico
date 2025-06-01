import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config:
    # Clave secreta
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev_jwt_secret")

    # Carpeta instance
    INSTANCE_PATH = os.path.join(BASE_DIR, 'instance')
    os.makedirs(INSTANCE_PATH, exist_ok=True)

    # Base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(INSTANCE_PATH, 'app.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Seguridad
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.getenv("FLASK_ENV") == "production"
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 86400  # 1 día

    # CORS
    CORS_HEADERS = "Content-Type"

    # Debug
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1"]

    # Entorno
    ENV = os.getenv("FLASK_ENV", "development")