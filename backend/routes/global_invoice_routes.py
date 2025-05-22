from flask import Blueprint, request, jsonify
from extensions import db
from models.global_invoice import GlobalInvoice
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

global_invoice_bp = Blueprint('global_invoice', __name__)

def generate_global_invoice_number():
    last_gi = GlobalInvoice.query.order_by(GlobalInvoice.id.desc()).first()
    if last_gi and last_gi.global_invoice_number.startswith("FG"):
        last_number = int(last_gi.global_invoice_number[2:])
        new_number = f"FG{last_number + 1:06d}"
    else:
        new_number = "FG000001"
    return new_number

@global_invoice_bp.route('/next-number', methods=['POST'])
def reserve_global_invoice_number():
    try:
        next_number = generate_global_invoice_number()
        return jsonify({'global_invoice_number': next_number}), 200
    except Exception as e:
        return jsonify({'message': f"Error reserving global invoice number: {str(e)}"}), 500

@global_invoice_bp.route('', methods=['GET'])
@jwt_required()
def get_global_invoices():
    global_invoices = GlobalInvoice.query.all()
    return jsonify([gi.to_dict() for gi in global_invoices])

@global_invoice_bp.route('', methods=['POST'])
@jwt_required()
def create_global_invoice():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        global_invoice_number = generate_global_invoice_number()
        global_invoice = GlobalInvoice(
            global_invoice_number=global_invoice_number,
            issue_date=data['issue_date'],
            client_id=data['client_id'],
            total_amount=data['total_amount']
        )
        db.session.add(global_invoice)
        db.session.commit()
        return jsonify(global_invoice.to_dict()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': f"Error creating global invoice: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f"Error creating global invoice: {str(e)}"}), 500

@global_invoice_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_global_invoice(id):
    global_invoice = GlobalInvoice.query.get_or_404(id)
    return jsonify(global_invoice.to_dict())

@global_invoice_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_global_invoice(id):
    data = request.get_json()
    global_invoice = GlobalInvoice.query.get_or_404(id)
    for key, value in data.items():
        setattr(global_invoice, key, value)
    db.session.commit()
    return jsonify(global_invoice.to_dict())

@global_invoice_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_global_invoice(id):
    global_invoice = GlobalInvoice.query.get_or_404(id)
    db.session.delete(global_invoice)
    db.session.commit()
    return '', 204
