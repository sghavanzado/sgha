# app.py 
from flask import Flask, jsonify, request, g, make_response
from flask_cors import CORS
from extensions import db, migrate, login_manager
from flask_jwt_extended import JWTManager  # Import JWTManager
from config import Config
from models.user import User, Role, initialize_permissions
from cli import register_commands
import logging
from logging.handlers import RotatingFileHandler
import os
import uuid
from routes import (
    auth, user_routes, product_routes, inventory_routes,
    inventory_reports_routes, order_routes, price_routes, warehouse_routes, role_routes,
    invoice_routes, accounting_routes, client_routes, services_routes  # Import client routes
)
from routes.location_routes import location_bp  # Import location routes
from routes.unit_routes import unit_bp  # Import unit routes
from routes.tax_routes import tax_bp  # Import tax routes
from routes.import_routes import import_bp  # Import import routes
from routes.supplier_routes import supplier_bp  # Updated import for supplier routes
from routes.services_routes import service_bp
from routes.receipt_routes import receipt_bp
from routes.debit_note_routes import debit_note_bp
from routes.global_invoice_routes import global_invoice_bp
from routes.self_billing_receipt_routes import self_billing_receipt_bp
from routes.transport_guide_routes import transport_guide_bp
from routes.shipping_guide_routes import shipping_guide_bp
from routes.order_note_routes import order_note_bp
from routes.delivery_note_routes import delivery_note_bp
from routes.payments_made_report import payments_made_report_bp
from routes.payments_pending_report import payments_pending_report_bp
from routes.item_billing_report import item_billing_report_bp
from routes.tax_map_report import tax_map_report_bp
from routes.billing_by_employee_report import billing_by_employee_report_bp
from routes.billing_report import billing_report_bp
from routes.tax_settlement_report import tax_settlement_report_bp
from routes.client_account_statement_report import client_account_statement_report_bp

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
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt = JWTManager(app)  # Initialize JWTManager

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
    @app.after_request
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

        return response

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
            response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
            return response

    # Middleware para inicializar request_id
    @app.before_request
    def initialize_request_id():
        g.request_id = str(uuid.uuid4())

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
    app.register_blueprint(services_routes.service_bp, url_prefix='/services')
    app.register_blueprint(inventory_routes.inventory_bp, url_prefix='/inventory')
    app.register_blueprint(supplier_bp, url_prefix='/suppliers')  # Updated supplier routes
    app.register_blueprint(order_routes.order_bp, url_prefix='/orders')
    app.register_blueprint(price_routes.price_bp, url_prefix='/prices')
    app.register_blueprint(inventory_reports_routes.inventory_reports_bp, url_prefix='/reports')
    app.register_blueprint(warehouse_routes.warehouse_bp, url_prefix='/warehouse')
    app.register_blueprint(role_routes.role_bp, url_prefix='/roles')
    app.register_blueprint(invoice_routes.invoice_bp, url_prefix='/invoices')
    app.register_blueprint(accounting_routes.accounting_bp, url_prefix='/accounting')
    app.register_blueprint(client_routes.client_bp, url_prefix='/clients')  # Register client routes
    app.register_blueprint(location_bp, url_prefix='/locations')  # Register location routes
    app.register_blueprint(unit_bp, url_prefix='/units')  # Register unit routes
    app.register_blueprint(tax_bp, url_prefix='/taxes')  # Register tax routes
    app.register_blueprint(import_bp, url_prefix='/import')  # Register import routes
    app.register_blueprint(receipt_bp, url_prefix='/receipts')
    app.register_blueprint(debit_note_bp, url_prefix='/debit-notes')
    app.register_blueprint(global_invoice_bp, url_prefix='/global-invoices')
    app.register_blueprint(self_billing_receipt_bp, url_prefix='/self-billing-receipts')
    app.register_blueprint(transport_guide_bp, url_prefix='/transport-guides')
    app.register_blueprint(shipping_guide_bp, url_prefix='/shipping-guides')
    app.register_blueprint(order_note_bp, url_prefix='/order-notes')
    app.register_blueprint(delivery_note_bp, url_prefix='/delivery-notes')
    app.register_blueprint(payments_made_report_bp)
    app.register_blueprint(payments_pending_report_bp)
    app.register_blueprint(item_billing_report_bp)
    app.register_blueprint(tax_map_report_bp)
    app.register_blueprint(billing_by_employee_report_bp)
    app.register_blueprint(billing_report_bp)
    app.register_blueprint(tax_settlement_report_bp)
    app.register_blueprint(client_account_statement_report_bp)

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG'],
        ssl_context='adhoc' if app.config.get('ENABLE_HTTPS') else None
    )