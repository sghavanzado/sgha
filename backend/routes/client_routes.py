from flask import Blueprint, jsonify, request
from extensions import db
from models.client import Client  # Ensure Client is imported from models.client
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError  # Add this import

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
    """Create a new client or multiple clients."""
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    if isinstance(data, list):  # Handle bulk creation
        clients = []
        for client_data in data:
            if not isinstance(client_data, dict):  # Ensure each item is a dictionary
                return jsonify({'message': 'Invalid data format for bulk creation'}), 400
            try:
                client = Client(**client_data)
                db.session.add(client)
                clients.append(client.to_dict())
            except IntegrityError as e:  # Handle duplicate key errors
                db.session.rollback()
                return jsonify({'message': f"Duplicate entry: {str(e.orig)}"}), 400
            except Exception as e:
                db.session.rollback()
                return jsonify({'message': f"Error creating client: {str(e)}"}), 400
        db.session.commit()
        return jsonify({'message': 'Clients created successfully', 'clients': clients}), 201

    elif isinstance(data, dict):  # Handle single creation
        try:
            client = Client(**data)
            db.session.add(client)
            db.session.commit()
            return jsonify(client.to_dict()), 201
        except IntegrityError as e:  # Handle duplicate key errors
            db.session.rollback()
            return jsonify({'message': f"Duplicate entry: {str(e.orig)}"}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f"Error creating client: {str(e)}"}), 400

    return jsonify({'message': 'Invalid data format'}), 400

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
