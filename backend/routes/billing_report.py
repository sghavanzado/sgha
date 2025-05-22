from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from extensions import db

billing_report_bp = Blueprint('billing_report', __name__)

@billing_report_bp.route('/api/billing-report', methods=['GET'])
@jwt_required()
def billing_report():
    # Suponiendo tabla invoices con: seller_name, invoice_number, client_name, issue_date, subtotal, tax, retention, total
    query = db.session.query(
        db.literal_column('seller_name'),
        db.literal_column('invoice_number'),
        db.literal_column('client_name'),
        db.literal_column('issue_date'),
        db.literal_column('subtotal'),
        db.literal_column('tax'),
        db.literal_column('retention'),
        db.literal_column('total')
    ).select_from(db.text('invoices'))

    results = query.all()

    rows = []
    total_subtotal = 0
    total_tax = 0
    total_retention = 0
    total_total = 0

    for row in results:
        rows.append({
            "seller_name": row.seller_name,
            "invoice_number": row.invoice_number,
            "client_name": row.client_name,
            "issue_date": row.issue_date,
            "subtotal": float(row.subtotal or 0),
            "tax": float(row.tax or 0),
            "retention": float(row.retention or 0),
            "total": float(row.total or 0),
        })
        total_subtotal += float(row.subtotal or 0)
        total_tax += float(row.tax or 0)
        total_retention += float(row.retention or 0)
        total_total += float(row.total or 0)

    return jsonify({
        "rows": rows,
        "summary": {
            "total_subtotal": total_subtotal,
            "total_tax": total_tax,
            "total_retention": total_retention,
            "total_total": total_total
        }
    })
