from flask import Blueprint, request, jsonify
from extensions import db
from models.debit_note import DebitNote
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

debit_note_bp = Blueprint('debit_note', __name__)

def generate_debit_note_number():
    last_dn = DebitNote.query.order_by(DebitNote.id.desc()).first()
    if last_dn and last_dn.debit_note_number.startswith("ND"):
        last_number = int(last_dn.debit_note_number[2:])
        new_number = f"ND{last_number + 1:06d}"
    else:
        new_number = "ND000001"
    return new_number

@debit_note_bp.route('/next-number', methods=['POST'])
def reserve_debit_note_number():
    try:
        next_number = generate_debit_note_number()
        return jsonify({'debit_note_number': next_number}), 200
    except Exception as e:
        return jsonify({'message': f"Error reserving debit note number: {str(e)}"}), 500

@debit_note_bp.route('', methods=['GET'])
@jwt_required()
def get_debit_notes():
    debit_notes = DebitNote.query.all()
    return jsonify([dn.to_dict() for dn in debit_notes])

@debit_note_bp.route('', methods=['POST'])
@jwt_required()
def create_debit_note():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        debit_note_number = generate_debit_note_number()
        debit_note = DebitNote(
            debit_note_number=debit_note_number,
            issue_date=data['issue_date'],
            client_id=data['client_id'],
            total_amount=data['total_amount']
        )
        db.session.add(debit_note)
        db.session.commit()
        return jsonify(debit_note.to_dict()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': f"Error creating debit note: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f"Error creating debit note: {str(e)}"}), 500

@debit_note_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_debit_note(id):
    debit_note = DebitNote.query.get_or_404(id)
    return jsonify(debit_note.to_dict())

@debit_note_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_debit_note(id):
    data = request.get_json()
    debit_note = DebitNote.query.get_or_404(id)
    for key, value in data.items():
        setattr(debit_note, key, value)
    db.session.commit()
    return jsonify(debit_note.to_dict())

@debit_note_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_debit_note(id):
    debit_note = DebitNote.query.get_or_404(id)
    db.session.delete(debit_note)
    db.session.commit()
    return '', 204
