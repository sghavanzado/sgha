from flask import Blueprint, request, jsonify
from extensions import db
from models.shipping_guide import ShippingGuide
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from datetime import datetime

shipping_guide_bp = Blueprint('shipping_guide', __name__)

def generate_guide_number():
    last_guide = ShippingGuide.query.order_by(ShippingGuide.id.desc()).first()
    if last_guide and last_guide.guide_number.startswith("GR"):
        last_number = int(last_guide.guide_number[2:])
        new_number = f"GR{last_number + 1:06d}"
    else:
        new_number = "GR000001"
    return new_number

@shipping_guide_bp.route('/next-number', methods=['POST'])
def reserve_guide_number():
    try:
        next_number = generate_guide_number()
        return jsonify({'guide_number': next_number}), 200
    except Exception as e:
        return jsonify({'message': f"Error reserving guide number: {str(e)}"}), 500

@shipping_guide_bp.route('', methods=['GET'])
@jwt_required()
def get_guides():
    guides = ShippingGuide.query.all()
    return jsonify([g.to_dict() for g in guides])

@shipping_guide_bp.route('', methods=['POST'])
@jwt_required()
def create_guide():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        guide_number = generate_guide_number()
        guide = ShippingGuide(
            guide_number=guide_number,
            issue_date=datetime.fromisoformat(data['issue_date']),
            client_id=data['client_id'],
            total_amount=data['total_amount'],
            vehicle_plate=data.get('vehicle_plate'),
            load_date=datetime.fromisoformat(data['load_date']) if data.get('load_date') else None,
            load_location=data.get('load_location'),
            load_address=data.get('load_address'),
            load_city=data.get('load_city'),
            load_postal_code=data.get('load_postal_code'),
            delivery_location=data.get('delivery_location'),
            delivery_address=data.get('delivery_address'),
            delivery_city=data.get('delivery_city'),
            delivery_postal_code=data.get('delivery_postal_code')
        )
        db.session.add(guide)
        db.session.commit()
        return jsonify(guide.to_dict()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': f"Error creating guide: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f"Error creating guide: {str(e)}"}), 500

@shipping_guide_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_guide(id):
    guide = ShippingGuide.query.get_or_404(id)
    return jsonify(guide.to_dict())

@shipping_guide_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_guide(id):
    data = request.get_json()
    guide = ShippingGuide.query.get_or_404(id)
    for key, value in data.items():
        setattr(guide, key, value)
    db.session.commit()
    return jsonify(guide.to_dict())

@shipping_guide_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_guide(id):
    guide = ShippingGuide.query.get_or_404(id)
    db.session.delete(guide)
    db.session.commit()
    return '', 204
