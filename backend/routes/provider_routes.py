from flask import Blueprint, jsonify, request
from models.provider import Provider
from extensions import db

provider_bp = Blueprint('provider_bp', __name__)

@provider_bp.route('', methods=['POST'])
def create_provider():
    try:
        data = request.json
        if not all(key in data for key in ('name', 'contact_info')):
            return jsonify({'error': 'Missing required fields'}), 400

        provider = Provider(
            name=data['name'],
            contact_info=data['contact_info'],
            payment_terms=data.get('payment_terms', ''),
            delivery_times=data.get('delivery_times', ''),
            active=data.get('active', True)
        )
        db.session.add(provider)
        db.session.commit()
        return jsonify(provider.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@provider_bp.route('', methods=['GET'])
def list_providers():
    try:
        providers = Provider.query.all()
        return jsonify([provider.to_dict() for provider in providers]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@provider_bp.route('/<int:provider_id>', methods=['GET'])
def get_provider(provider_id):
    provider = Provider.query.get(provider_id)
    if not provider:
        return jsonify({'error': 'Provider not found'}), 404
    return jsonify(provider.to_dict()), 200