from flask import Blueprint, jsonify, request
from extensions import db
from models.client import Client
from flask_jwt_extended import jwt_required

client_bp = Blueprint('clients', __name__, url_prefix='/clients')

@client_bp.route('/', methods=['GET'])
@jwt_required()
def get_clients():
    """Get all clients."""
    clients = Client.query.all()
    return jsonify([client.to_dict() for client in clients]), 200

@client_bp.route('/', methods=['POST'])
@jwt_required()
def create_client():
    """Create a new client."""
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    client = Client(**data)
    db.session.add(client)
    db.session.commit()
    return jsonify(client.to_dict()), 201

@client_bp.route('/<int:client_id>', methods=['PUT'])
@jwt_required()
def update_client(client_id):
    """Update an existing client."""
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'message': 'Client not found'}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(client, key, value)

    db.session.commit()
    return jsonify(client.to_dict()), 200

@client_bp.route('/<int:client_id>', methods=['DELETE'])
@jwt_required()
def delete_client(client_id):
    """Delete a client."""
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'message': 'Client not found'}), 404

    db.session.delete(client)
    db.session.commit()
    return jsonify({'message': 'Client deleted'}), 200
