from flask import Blueprint, request, jsonify
from extensions import db
from models.invoice import Invoice
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

invoice_bp = Blueprint('invoice', __name__)

def generate_invoice_number():
    """Generate a new invoice number starting with 'FA'."""
    last_invoice = Invoice.query.order_by(Invoice.id.desc()).first()
    if last_invoice and last_invoice.invoice_number.startswith("FA"):
        last_number = int(last_invoice.invoice_number[2:])
        new_number = f"FA{last_number + 1:06d}"
    else:
        new_number = "FA000001"
    return new_number

@invoice_bp.route('/next-number', methods=['POST'])
def reserve_invoice_number():
    """Reserve and return the next invoice number."""
    try:
        next_number = generate_invoice_number()
        return jsonify({'invoice_number': next_number}), 200
    except Exception as e:
        return jsonify({'message': f"Error reserving invoice number: {str(e)}"}), 500

# Ruta para obtener todas las facturas
@invoice_bp.route('', methods=['GET'])
@jwt_required()
def get_invoices():
    invoices = Invoice.query.all()
    return jsonify([invoice.to_dict() for invoice in invoices])

# Ruta para crear una nueva factura
@invoice_bp.route('', methods=['POST'])
@jwt_required()
def create_invoice():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        # Generate the invoice number only when creating the invoice
        invoice_number = generate_invoice_number()
        invoice = Invoice(
            invoice_number=invoice_number,
            issue_date=data['issue_date'],
            due_date=data['due_date'],
            total_amount=data['total_amount'],
            status=data['status'],
            client_id=data['client_id'],
            items=data['items']
        )
        db.session.add(invoice)
        db.session.commit()
        return jsonify(invoice.to_dict()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': f"Error creating invoice: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f"Error creating invoice: {str(e)}"}), 500

# Ruta para obtener una factura por ID
@invoice_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    return jsonify(invoice.to_dict())

# Ruta para actualizar una factura por ID
@invoice_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_invoice(id):
    data = request.get_json()
    invoice = Invoice.query.get_or_404(id)
    for key, value in data.items():
        setattr(invoice, key, value)
    db.session.commit()
    return jsonify(invoice.to_dict())

# Ruta para eliminar una factura por ID
@invoice_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    db.session.delete(invoice)
    db.session.commit()
    return '', 204
