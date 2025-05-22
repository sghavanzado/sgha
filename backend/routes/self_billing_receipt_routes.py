from flask import Blueprint, request, jsonify
from extensions import db
from models.self_billing_receipt import SelfBillingReceipt
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

self_billing_receipt_bp = Blueprint('self_billing_receipt', __name__)

def generate_self_billing_receipt_number():
    last_sbr = SelfBillingReceipt.query.order_by(SelfBillingReceipt.id.desc()).first()
    if last_sbr and last_sbr.self_billing_receipt_number.startswith("AFR"):
        last_number = int(last_sbr.self_billing_receipt_number[3:])
        new_number = f"AFR{last_number + 1:06d}"
    else:
        new_number = "AFR000001"
    return new_number

@self_billing_receipt_bp.route('/next-number', methods=['POST'])
def reserve_self_billing_receipt_number():
    try:
        next_number = generate_self_billing_receipt_number()
        return jsonify({'self_billing_receipt_number': next_number}), 200
    except Exception as e:
        return jsonify({'message': f"Error reserving self-billing receipt number: {str(e)}"}), 500

@self_billing_receipt_bp.route('', methods=['GET'])
@jwt_required()
def get_self_billing_receipts():
    receipts = SelfBillingReceipt.query.all()
    return jsonify([r.to_dict() for r in receipts])

@self_billing_receipt_bp.route('', methods=['POST'])
@jwt_required()
def create_self_billing_receipt():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        self_billing_receipt_number = generate_self_billing_receipt_number()
        receipt = SelfBillingReceipt(
            self_billing_receipt_number=self_billing_receipt_number,
            issue_date=data['issue_date'],
            client_id=data['client_id'],
            total_amount=data['total_amount']
        )
        db.session.add(receipt)
        db.session.commit()
        return jsonify(receipt.to_dict()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': f"Error creating self-billing receipt: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f"Error creating self-billing receipt: {str(e)}"}), 500

@self_billing_receipt_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_self_billing_receipt(id):
    receipt = SelfBillingReceipt.query.get_or_404(id)
    return jsonify(receipt.to_dict())

@self_billing_receipt_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_self_billing_receipt(id):
    data = request.get_json()
    receipt = SelfBillingReceipt.query.get_or_404(id)
    for key, value in data.items():
        setattr(receipt, key, value)
    db.session.commit()
    return jsonify(receipt.to_dict())

@self_billing_receipt_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_self_billing_receipt(id):
    receipt = SelfBillingReceipt.query.get_or_404(id)
    db.session.delete(receipt)
    db.session.commit()
    return '', 204
