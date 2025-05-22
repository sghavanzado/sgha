from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from extensions import db

tax_settlement_report_bp = Blueprint('tax_settlement_report', __name__)

@tax_settlement_report_bp.route('/api/tax-settlement-report', methods=['GET'])
@jwt_required()
def tax_settlement_report():
    month = request.args.get('month')
    year = request.args.get('year')

    # Determinar intervalo de datas
    try:
        month = int(month)
        year = int(year)
        from_date = f"{year}-{month:02d}-01"
        if month == 12:
            to_date = f"{year}-12-31"
        else:
            from datetime import datetime, timedelta
            next_month = datetime(year, month, 1).replace(day=28) + timedelta(days=4)
            last_day = (next_month - timedelta(days=next_month.day)).day
            to_date = f"{year}-{month:02d}-{last_day:02d}"
    except Exception:
        from_date = None
        to_date = None

    # Suponiendo tabla invoices con: invoice_number, issue_date, total, stamp_tax (imposto de selo)
    query = db.session.query(
        db.literal_column('invoice_number'),
        db.literal_column('issue_date'),
        db.literal_column('total').label('total'),
        db.literal_column('stamp_tax').label('stamp_tax')
    ).select_from(db.text('invoices'))

    filters = []
    if from_date:
        filters.append(db.literal_column('issue_date') >= from_date)
    if to_date:
        filters.append(db.literal_column('issue_date') <= to_date)

    if filters:
        query = query.filter(*filters)

    results = query.all()

    rows = []
    total_value = 0
    total_stamp_tax = 0

    for row in results:
        rows.append({
            "document": row.invoice_number,
            "total": float(row.total or 0),
            "stamp_tax": float(row.stamp_tax or 0),
        })
        total_value += float(row.total or 0)
        total_stamp_tax += float(row.stamp_tax or 0)

    return jsonify({
        "rows": rows,
        "summary": {
            "total": total_value,
            "total_stamp_tax": total_stamp_tax
        }
    })
