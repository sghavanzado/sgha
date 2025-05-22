from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from extensions import db

item_billing_report_bp = Blueprint('item_billing_report', __name__)

@item_billing_report_bp.route('/api/item-billing-report', methods=['GET'])
@jwt_required()
def item_billing_report():
    item_filter = request.args.get('item')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    # Ajusta las fechas si no se proveen
    try:
        if date_from:
            date_from = date_from + " 00:00:00"
        if date_to:
            date_to = date_to + " 23:59:59"
    except Exception:
        date_from = None
        date_to = None

    # Suponiendo que hay una tabla Invoice y una tabla InvoiceItem relacionada
    # InvoiceItem: id, invoice_id, product_code, description, quantity, unit_price, tax_rate, tax_amount, total
    query = db.session.query(
        db.literal_column('product_code'),
        db.literal_column('description'),
        func.sum(db.literal_column('quantity')).label('quantity'),
        func.avg(db.literal_column('unit_price')).label('avg_price'),
        func.sum(db.literal_column('quantity') * db.literal_column('unit_price')).label('value'),
        func.sum(db.literal_column('tax_amount')).label('tax'),
        func.sum(db.literal_column('total')).label('total')
    ).select_from(db.text('invoice_items'))

    filters = []
    if item_filter:
        filters.append(db.literal_column('product_code') == item_filter)
    if date_from:
        filters.append(db.literal_column('created_at') >= date_from)
    if date_to:
        filters.append(db.literal_column('created_at') <= date_to)

    if filters:
        query = query.filter(*filters)

    query = query.group_by(db.literal_column('product_code'), db.literal_column('description'))

    results = query.all()

    rows = []
    total_value = 0
    total_tax = 0
    total_total = 0
    total_quantity = 0

    for row in results:
        rows.append({
            "item": row.product_code,
            "description": row.description,
            "quantity": float(row.quantity or 0),
            "avg_price": float(row.avg_price or 0),
            "value": float(row.value or 0),
            "tax": float(row.tax or 0),
            "total": float(row.total or 0),
        })
        total_quantity += float(row.quantity or 0)
        total_value += float(row.value or 0)
        total_tax += float(row.tax or 0)
        total_total += float(row.total or 0)

    return jsonify({
        "rows": rows,
        "summary": {
            "total_quantity": total_quantity,
            "total_value": total_value,
            "total_tax": total_tax,
            "total_total": total_total
        }
    })
