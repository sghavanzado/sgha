from flask import Blueprint, jsonify, request
from extensions import db
from models.services import Service
from sqlalchemy.exc import IntegrityError
import logging  # Add logging for error handling

service_bp = Blueprint('service_bp', __name__, url_prefix='/services')

@service_bp.route('/', methods=['POST'])
def create_service():
    """Create a new service or multiple services."""
    try:
        data = request.get_json()
        if not data:
            logging.error("No data provided in request")
            return jsonify({'message': 'No data provided'}), 400
    except Exception as e:
        logging.error(f"Invalid JSON format: {str(e)}")
        return jsonify({'message': 'Invalid JSON format'}), 400

    if isinstance(data, list):  # Handle bulk creation
        services = []
        for service_data in data:
            if not isinstance(service_data, dict):  # Ensure each item is a dictionary
                logging.error(f"Invalid data format for bulk creation: {service_data}")
                return jsonify({'message': 'Invalid data format for bulk creation'}), 400
            try:
                service = Service(
                    name=service_data['name'],
                    description=service_data.get('description', ''),
                    price=service_data['price'],
                    category=service_data['category'],
                    duration=service_data.get('duration', ''),
                    active=service_data.get('active', True)
                )
                db.session.add(service)
                services.append(service.to_dict())
            except IntegrityError as e:
                db.session.rollback()
                logging.error(f"Duplicate entry detected: {str(e)}")
                return jsonify({'message': f"Duplicate entry: {str(e)}"}), 400
            except Exception as e:
                db.session.rollback()
                logging.error(f"Error creating service: {str(e)}")
                return jsonify({'message': f"Error creating service: {str(e)}"}), 400
        db.session.commit()
        return jsonify({'message': 'Services created successfully', 'services': services}), 201

    elif isinstance(data, dict):  # Handle single creation
        try:
            service = Service(
                name=data['name'],
                description=data.get('description', ''),
                price=data['price'],
                category=data['category'],
                duration=data.get('duration', ''),
                active=data.get('active', True)
            )
            db.session.add(service)
            db.session.commit()
            return jsonify(service.to_dict()), 201
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"Duplicate entry detected: {str(e)}")
            return jsonify({'message': f"Duplicate entry: {str(e)}"}), 400
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating service: {str(e)}")
            return jsonify({'message': f"Error creating service: {str(e)}"}), 400

    logging.error(f"Invalid data format: {data}")
    return jsonify({'message': 'Invalid data format'}), 400

@service_bp.route('/', methods=['GET'])
def list_services():
    services = Service.query.all()
    return jsonify([service.to_dict() for service in services]), 200

@service_bp.route('/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    data = request.get_json()
    service.name = data.get('name', service.name)
    service.description = data.get('description', service.description)
    service.price = data.get('price', service.price)
    service.category = data.get('category', service.category)
    service.duration = data.get('duration', service.duration)
    service.active = data.get('active', service.active)

    db.session.commit()
    return jsonify(service.to_dict()), 200

@service_bp.route('/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted successfully'}), 200
