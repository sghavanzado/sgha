from flask import Blueprint, jsonify, request
from extensions import db
from models.tax import TaxType
from flask_jwt_extended import jwt_required

tax_bp = Blueprint('taxes', __name__, url_prefix='/taxes')

@tax_bp.route('/', methods=['GET'])
@jwt_required()
def get_tax_types():
    """Get all tax types."""
    tax_types = TaxType.query.all()
    return jsonify([tax_type.to_dict() for tax_type in tax_types]), 200

@tax_bp.route('/', methods=['POST'])
@jwt_required()
def create_tax_type():
    """Create a new tax type."""
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    tax_type = TaxType(**data)
    db.session.add(tax_type)
    db.session.commit()
    return jsonify(tax_type.to_dict()), 201

@tax_bp.route('/<int:tax_id>', methods=['PUT'])
@jwt_required()
def update_tax_type(tax_id):
    """Update an existing tax type."""
    tax_type = TaxType.query.get(tax_id)
    if not tax_type:
        return jsonify({'message': 'Tax type not found'}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(tax_type, key, value)

    db.session.commit()
    return jsonify(tax_type.to_dict()), 200

@tax_bp.route('/<int:tax_id>', methods=['DELETE'])
@jwt_required()
def delete_tax_type(tax_id):
    """Delete a tax type."""
    tax_type = TaxType.query.get(tax_id)
    if not tax_type:
        return jsonify({'message': 'Tax type not found'}), 404

    db.session.delete(tax_type)
    db.session.commit()
    return jsonify({'message': 'Tax type deleted'}), 200
