from flask import Blueprint, request, jsonify
from extensions import db
from models.invoice import Invoice
from flask_jwt_extended import jwt_required

invoice_bp = Blueprint('invoice', __name__)

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
    data = request.get_json()
    invoice = Invoice(**data)
    db.session.add(invoice)
    db.session.commit()
    return jsonify(invoice.to_dict()), 201

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
