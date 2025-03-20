from flask import Blueprint, request, jsonify
from extensions import db
from models.client import Client
from models.accounting import Supplier, Product, Invoice
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required

import_bp = Blueprint('import', __name__, url_prefix='/api/import')

def validate_json(data, required_keys):
    """Validate JSON structure."""
    if not isinstance(data, list):
        return False, "JSON must be an array of objects."
    for item in data:
        if not all(key in item for key in required_keys):
            return False, f"Missing required keys: {required_keys}"
    return True, None

def bulk_insert(model, data):
    """Perform bulk insert with SQLAlchemy."""
    try:
        db.session.bulk_insert_mappings(model, data)
        db.session.commit()
        return True, None
    except IntegrityError as e:
        db.session.rollback()
        return False, str(e)

@import_bp.route('/customers', methods=['POST'])
@jwt_required()
def import_customers():
    """Import customers."""
    data = request.get_json()
    required_keys = ['name', 'nif', 'address', 'city', 'state', 'country', 'phone', 'email']
    is_valid, error = validate_json(data, required_keys)
    if not is_valid:
        return jsonify({'message': error}), 400

    success, error = bulk_insert(Client, data)
    if not success:
        return jsonify({'message': f"Error importing customers: {error}"}), 400

    return jsonify({'message': 'Customers imported successfully'}), 201

@import_bp.route('/suppliers', methods=['POST'])
@jwt_required()
def import_suppliers():
    """Import suppliers."""
    data = request.get_json()
    required_keys = ['name', 'nif', 'address', 'phone', 'contact_first_name', 'contact_last_name']
    is_valid, error = validate_json(data, required_keys)
    if not is_valid:
        return jsonify({'message': error}), 400

    success, error = bulk_insert(Supplier, data)
    if not success:
        return jsonify({'message': f"Error importing suppliers: {error}"}), 400

    return jsonify({'message': 'Suppliers imported successfully'}), 201

@import_bp.route('/products', methods=['POST'])
@jwt_required()
def import_products():
    """Import products."""
    data = request.get_json()
    required_keys = ['sku', 'name', 'price', 'unit', 'category', 'stock']
    is_valid, error = validate_json(data, required_keys)
    if not is_valid:
        return jsonify({'message': error}), 400

    success, error = bulk_insert(Product, data)
    if not success:
        return jsonify({'message': f"Error importing products: {error}"}), 400

    return jsonify({'message': 'Products imported successfully'}), 201

@import_bp.route('/invoices', methods=['POST'])
@jwt_required()
def import_invoices():
    """Import invoices."""
    data = request.get_json()
    required_keys = ['invoice_number', 'issue_date', 'client_id', 'total_amount', 'items']
    is_valid, error = validate_json(data, required_keys)
    if not is_valid:
        return jsonify({'message': error}), 400

    success, error = bulk_insert(Invoice, data)
    if not success:
        return jsonify({'message': f"Error importing invoices: {error}"}), 400

    return jsonify({'message': 'Invoices imported successfully'}), 201

@import_bp.route('/all', methods=['POST'])
@jwt_required()
def import_all():
    """Import all data."""
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({'message': 'Invalid JSON structure. Expected a dictionary.'}), 400

    results = {}
    for model_name, model_data in data.items():
        if model_name == 'customers':
            success, error = bulk_insert(Client, model_data)
        elif model_name == 'suppliers':
            success, error = bulk_insert(Supplier, model_data)
        elif model_name == 'products':
            success, error = bulk_insert(Product, model_data)
        elif model_name == 'invoices':
            success, error = bulk_insert(Invoice, model_data)
        else:
            results[model_name] = 'Unknown model'
            continue

        if success:
            results[model_name] = 'Imported successfully'
        else:
            results[model_name] = f"Error: {error}"

    return jsonify(results), 200
