from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from extensions import db

billing_by_employee_report_bp = Blueprint('billing_by_employee_report', __name__)

@billing_by_employee_report_bp.route('/api/billing-by-employee-report', methods=['GET'])
@jwt_required()
def billing_by_employee_report():
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

    # Suponiendo tabla invoices con seller_name (colaborador), invoice_number, client_name, issue_date, subtotal, retention
    query = db.session.query(
        db.literal_column('seller_name'),
        db.literal_column('invoice_number'),
        db.literal_column('client_name'),
        db.literal_column('issue_date'),
        db.literal_column('subtotal'),
        db.literal_column('retention')
    ).select_from(db.text('invoices'))

    filters = []
    if date_from:
        filters.append(db.literal_column('issue_date') >= date_from)
    if date_to:
        filters.append(db.literal_column('issue_date') <= date_to)

    if filters:
        query = query.filter(*filters)

    results = query.all()

    rows = []
    for row in results:
        rows.append({
            "seller_name": row.seller_name,
            "invoice_number": row.invoice_number,
            "client_name": row.client_name,
            "issue_date": row.issue_date,
            "subtotal": float(row.subtotal or 0),
            "retention": float(row.retention or 0),
        })

    return jsonify({
        "rows": rows
    })
