import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde .env

class Config:
    # Configuración Base
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or os.urandom(32)
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    
    # Configuración de Base de Datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgr3s@localhost:5432/sghadb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'max_overflow': 20
    }
    
    # Configuración JWT
    JWT_TOKEN_LOCATION = ['headers', 'cookies']  # Aceptar tokens en headers y cookies
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=45)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_COOKIE_SECURE = False  # True en producción
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SAMESITE = 'Lax'  # Prevenir CSRF
    
    
    # Configuración CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5173').split(',')
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_EXPOSE_HEADERS = ['Content-Type', 'X-Total-Count', 'X-Requested-With', 'Authorization'] 
    
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    # Configuración de Seguridad de Sesiones
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora
    
    # Configuración HTTPS
    ENABLE_HTTPS = os.environ.get('ENABLE_HTTPS', 'false').lower() == 'true'
    
    # Configuración de Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')
    LOG_MAX_BYTES = 1024 * 1024 * 10  # 10 MB
    LOG_BACKUP_COUNT = 10
    
    # Configuración de Ratelimit
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'memory://')
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_DEFAULT = '500 per hour'
    
    # Configuración de Auditoría
    AUDIT_LOG_ENABLED = True
    AUDIT_LOG_FILE = 'logs/audit.log'

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 30
    }
    ENABLE_HTTPS = True

class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'max_overflow': 10
    }

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    JWT_BLACKLIST_ENABLED = False