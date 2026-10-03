import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-secret-key-change-in-prod')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', f"sqlite:///{BASE_DIR / 'database' / 'customer_service.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    JWT_SECRET = os.environ.get('JWT_SECRET', 'jwt-secret-token-key-2026')
    SOCKETIO_PING_TIMEOUT = 30
    SOCKETIO_PING_INTERVAL = 15

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
