from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from extensions import db

tax_map_report_bp = Blueprint('tax_map_report', __name__)

@tax_map_report_bp.route('/api/tax-map-report', methods=['GET'])
@jwt_required()
def tax_map_report():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    try:
        if date_from:
            date_from = date_from + " 00:00:00"
        if date_to:
            date_to = date_to + " 23:59:59"
    except Exception:
        date_from = None
        date_to = None

    # Suponiendo tabla invoice_items con tax_rate, tax_amount, y taxable_base (incidência)
    query = db.session.query(
        db.literal_column('tax_rate'),
        func.sum(db.literal_column('taxable_base')).label('incidencia'),
        func.sum(db.literal_column('tax_amount')).label('total_iva')
    ).select_from(db.text('invoice_items'))

    filters = []
    if date_from:
        filters.append(db.literal_column('created_at') >= date_from)
    if date_to:
        filters.append(db.literal_column('created_at') <= date_to)

    if filters:
        query = query.filter(*filters)

    query = query.group_by(db.literal_column('tax_rate'))

    results = query.all()

    rows = []
    total_iva = 0

    for row in results:
        rows.append({
            "tax_rate": float(row.tax_rate or 0),
            "incidencia": float(row.incidencia or 0),
            "total_iva": float(row.total_iva or 0),
        })
        total_iva += float(row.total_iva or 0)

    return jsonify({
        "rows": rows,
        "total_iva": total_iva
    })
