from flask import Blueprint, request, jsonify
from extensions import db
from models.delivery_note import DeliveryNote
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from datetime import datetime

delivery_note_bp = Blueprint('delivery_note', __name__)

def generate_delivery_note_number():
    last_note = DeliveryNote.query.order_by(DeliveryNote.id.desc()).first()
    if last_note and last_note.delivery_note_number.startswith("ND"):
        last_number = int(last_note.delivery_note_number[2:])
        new_number = f"ND{last_number + 1:06d}"
    else:
        new_number = "ND000001"
    return new_number

@delivery_note_bp.route('/next-number', methods=['POST'])
def reserve_delivery_note_number():
    try:
        next_number = generate_delivery_note_number()
        return jsonify({'delivery_note_number': next_number}), 200
    except Exception as e:
        return jsonify({'message': f"Error reserving delivery note number: {str(e)}"}), 500

@delivery_note_bp.route('', methods=['GET'])
@jwt_required()
def get_delivery_notes():
    notes = DeliveryNote.query.all()
    return jsonify([n.to_dict() for n in notes])

@delivery_note_bp.route('', methods=['POST'])
@jwt_required()
def create_delivery_note():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        delivery_note_number = generate_delivery_note_number()
        note = DeliveryNote(
            delivery_note_number=delivery_note_number,
            delivery_date=datetime.fromisoformat(data['delivery_date']),
            delivery_location=data.get('delivery_location'),
            issue_date=datetime.fromisoformat(data['issue_date']),
            due_date=data.get('due_date'),
            reference=data.get('reference'),
            series=data.get('series'),
            currency=data.get('currency'),
            notes=data.get('notes'),
            retention_percent=data.get('retention_percent'),
            client_id=data['client_id'],
            items=data['items']
        )
        db.session.add(note)
        db.session.commit()
        return jsonify(note.to_dict()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': f"Error creating delivery note: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f"Error creating delivery note: {str(e)}"}), 500

@delivery_note_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_delivery_note(id):
    note = DeliveryNote.query.get_or_404(id)
    return jsonify(note.to_dict())

@delivery_note_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_delivery_note(id):
    data = request.get_json()
    note = DeliveryNote.query.get_or_404(id)
    for key, value in data.items():
        setattr(note, key, value)
    db.session.commit()
    return jsonify(note.to_dict())

@delivery_note_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_delivery_note(id):
    note = DeliveryNote.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return '', 204
