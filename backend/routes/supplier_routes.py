import logging  # Add this import
from flask import Blueprint, jsonify, request
from extensions import db
from models.supplier import Supplier
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError  # Add this import

supplier_bp = Blueprint('suppliers', __name__, url_prefix='/suppliers')

@supplier_bp.route('/', methods=['GET'])
@jwt_required()
def get_suppliers():
    """Get all suppliers."""
    suppliers = Supplier.query.all()
    return jsonify([supplier.to_dict() for supplier in suppliers]), 200

@supplier_bp.route('/', methods=['POST'])
@jwt_required()
def create_supplier():
    """Create a new supplier or multiple suppliers."""
    try:
        data = request.get_json()
        if not data:
            logging.error("No data provided in request")
            return jsonify({'message': 'No data provided'}), 400
    except Exception as e:
        logging.error(f"Invalid JSON format: {str(e)}")
        return jsonify({'message': 'Invalid JSON format'}), 400

    if isinstance(data, list):  # Handle bulk creation
        suppliers = []
        for supplier_data in data:
            if not isinstance(supplier_data, dict):  # Ensure each item is a dictionary
                logging.error(f"Invalid data format for bulk creation: {supplier_data}")
                return jsonify({'message': 'Invalid data format for bulk creation'}), 400
            if Supplier.query.filter_by(nif=supplier_data.get('nif')).first():  # Check for duplicate NIF
                logging.error(f"Duplicate NIF detected: {supplier_data.get('nif')}")
                return jsonify({'message': f"Duplicate NIF: {supplier_data.get('nif')}"}), 400
            try:
                supplier = Supplier(**supplier_data)
                db.session.add(supplier)
                suppliers.append(supplier.to_dict())
            except Exception as e:
                db.session.rollback()
                logging.error(f"Error creating supplier: {str(e)}")
                return jsonify({'message': f"Error creating supplier: {str(e)}"}), 400
        db.session.commit()
        return jsonify({'message': 'Suppliers created successfully', 'suppliers': suppliers}), 201

    elif isinstance(data, dict):  # Handle single creation
        if Supplier.query.filter_by(nif=data.get('nif')).first():  # Check for duplicate NIF
            logging.error(f"Duplicate NIF detected: {data.get('nif')}")
            return jsonify({'message': f"Duplicate NIF: {data.get('nif')}"}), 400
        try:
            supplier = Supplier(**data)
            db.session.add(supplier)
            db.session.commit()
            return jsonify(supplier.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating supplier: {str(e)}")
            return jsonify({'message': f"Error creating supplier: {str(e)}"}), 400

    logging.error(f"Invalid data format: {data}")
    return jsonify({'message': 'Invalid data format'}), 400

@supplier_bp.route('/<int:supplier_id>', methods=['PUT'])
@jwt_required()
def update_supplier(supplier_id):
    """Update an existing supplier."""
    supplier = Supplier.query.get(supplier_id)
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(supplier, key, value)

    db.session.commit()
    return jsonify(supplier.to_dict()), 200

@supplier_bp.route('/<int:supplier_id>', methods=['DELETE'])
@jwt_required()
def delete_supplier(supplier_id):
    """Delete a supplier."""
    supplier = Supplier.query.get(supplier_id)
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404

    db.session.delete(supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier deleted'}), 200
