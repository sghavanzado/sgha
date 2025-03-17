from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from extensions import db, jwt, migrate
from config import Config
from models.user import User, Role, initialize_permissions
from cli import register_commands
import logging
from logging.handlers import RotatingFileHandler
import os
from routes import (
    auth, user_routes, product_routes, inventory_routes,
    inventory_reports_routes, order_routes, provider_routes,
    price_routes, warehouse_routes, role_routes,
    invoice_routes, accounting_routes
)

def create_app():
    # Crear instancia de Flask
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configurar CORS
    CORS(app, resources={r"/*": {"origins": app.config['CORS_ORIGINS']}})

    # Configurar logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Inicio de la aplicación')


    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Registrar comandos CLI
    register_commands(app)

    # Configuración inicial de permisos
    with app.app_context():
        try:
            initialize_permissions(app)
            app.logger.info("Permisos y roles inicializados correctamente")
        except Exception as e:
            app.logger.error(f"Error inicializando permisos: {str(e)}")
            raise

    # Configurar manejadores de errores JWT
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        app.logger.warning(f'Intento de acceso con token inválido: {error}')
        return jsonify({
            'error': 'Token inválido',
            'message': 'La autenticación falló'
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        app.logger.warning(f'Token expirado para el usuario: {jwt_payload["sub"]}')
        return jsonify({
            'error': 'Token expirado',
            'message': 'Renueve su token de acceso'
        }), 401

    # Middleware de seguridad global
    # Reemplazar el middleware de seguridad actual con este código
    @app.after_request  # Cambiar de before_request a after_request
    def security_middleware(response):
        """Middleware para agregar headers de seguridad a TODAS las respuestas"""
        # Headers de seguridad
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
    
    # Headers CORS (solo desarrollo)
        if app.config.get('ENV') == 'development':
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
    
        return response  # Asegurar retornar la respuesta modificada
    
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With") 
            response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
            return response
    

    # Middleware de autenticación global
    @app.before_request
    def check_authentication():
         # Permitir solicitudes OPTIONS sin autenticación
        if request.method == 'OPTIONS':
            return
        # Rutas excluidas de autenticación
        excluded_paths = [
            '/auth/login',
            '/auth/refresh',
            '/auth/register',
            '/docs', 
            '/spec'
        ]
        
        if request.path in excluded_paths:
            return

        # Verificar token JWT
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            app.logger.error('Intento de acceso sin token')
            return jsonify({'error': 'Acceso no autorizado'}), 401

        try:
            token = auth_header.split(" ")[1]
            jwt_data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            user = User.query.get(jwt_data['sub'])
            
            if not user or not user.is_active:
                raise Exception('Usuario no existe o está inactivo')
            
            g.current_user = user
            app.logger.info(f'Acceso autorizado para: {user.email} | ID: {g.request_id}')

        except Exception as e:
            app.logger.error(f'Error de autenticación: {str(e)} | ID: {g.request_id}')
            return jsonify({
                'error': 'Error de autenticación',
                'message': str(e),
                'request_id': g.request_id
            }), 401

    # Registrar blueprints
    register_blueprints(app)

    # Manejador de errores global
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Recurso no encontrado',
            'request_id': g.get('request_id', '')
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'error': 'Error interno del servidor',
            'request_id': g.get('request_id', '')
        }), 500

    return app

def register_blueprints(app):
    app.register_blueprint(auth.auth_bp, url_prefix='/auth')
    app.register_blueprint(user_routes.user_bp, url_prefix='/users')
    app.register_blueprint(product_routes.product_bp, url_prefix='/products')
    app.register_blueprint(inventory_routes.inventory_bp, url_prefix='/inventory')
    app.register_blueprint(provider_routes.provider_bp, url_prefix='/providers')
    app.register_blueprint(order_routes.order_bp, url_prefix='/orders')
    app.register_blueprint(price_routes.price_bp, url_prefix='/prices')
    app.register_blueprint(inventory_reports_routes.inventory_reports_bp, url_prefix='/reports')
    app.register_blueprint(warehouse_routes.warehouse_bp, url_prefix='/warehouse')
    app.register_blueprint(role_routes.role_bp, url_prefix='/roles')
    app.register_blueprint(invoice_routes.invoice_bp, url_prefix='/invoices')
    app.register_blueprint(accounting_routes.accounting_bp, url_prefix='/accounting')

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG'],
        ssl_context='adhoc' if app.config.get('ENABLE_HTTPS') else None
    )