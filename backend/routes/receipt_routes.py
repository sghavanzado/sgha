from flask import Blueprint, request, jsonify
from extensions import db
from models.receipt import Receipt
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

receipt_bp = Blueprint('receipt', __name__)

def generate_receipt_number():
    last_receipt = Receipt.query.order_by(Receipt.id.desc()).first()
    if last_receipt and last_receipt.receipt_number.startswith("RC"):
        last_number = int(last_receipt.receipt_number[2:])
        new_number = f"RC{last_number + 1:06d}"
    else:
        new_number = "RC000001"
    return new_number

@receipt_bp.route('/next-number', methods=['POST'])
def reserve_receipt_number():
    try:
        next_number = generate_receipt_number()
        return jsonify({'receipt_number': next_number}), 200
    except Exception as e:
        return jsonify({'message': f"Error reserving receipt number: {str(e)}"}), 500

@receipt_bp.route('', methods=['GET'])
@jwt_required()
def get_receipts():
    receipts = Receipt.query.all()
    return jsonify([receipt.to_dict() for receipt in receipts])

@receipt_bp.route('', methods=['POST'])
@jwt_required()
def create_receipt():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        receipt_number = generate_receipt_number()
        receipt = Receipt(
            receipt_number=receipt_number,
            issue_date=data['issue_date'],
            client_id=data['client_id'],
            total_amount=data['total_amount']
        )
        db.session.add(receipt)
        db.session.commit()
        return jsonify(receipt.to_dict()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': f"Error creating receipt: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f"Error creating receipt: {str(e)}"}), 500

@receipt_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_receipt(id):
    receipt = Receipt.query.get_or_404(id)
    return jsonify(receipt.to_dict())

@receipt_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_receipt(id):
    data = request.get_json()
    receipt = Receipt.query.get_or_404(id)
    for key, value in data.items():
        setattr(receipt, key, value)
    db.session.commit()
    return jsonify(receipt.to_dict())

@receipt_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_receipt(id):
    receipt = Receipt.query.get_or_404(id)
    db.session.delete(receipt)
    db.session.commit()
    return '', 204
