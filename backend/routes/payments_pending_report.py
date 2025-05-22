from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.client import Client
from models.invoice import Invoice
from datetime import datetime

payments_pending_report_bp = Blueprint('payments_pending_report', __name__)

@payments_pending_report_bp.route('/api/payments-pending-report', methods=['GET'])
@jwt_required()
def payments_pending_report():
    client_id = request.args.get('client_id')
    date_str = request.args.get('date')
    try:
        report_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else datetime.utcnow().date()
    except Exception:
        report_date = datetime.utcnow().date()

    query = db.session.query(
        Client.name.label('client_name'),
        Invoice.invoice_number,
        Invoice.due_date,
        Invoice.total_amount,
        Invoice.status
    ).join(Invoice, Invoice.client_id == Client.id)\
     .filter(Invoice.due_date <= report_date)

    if client_id and client_id != "all":
        query = query.filter(Client.id == int(client_id))

    results = query.all()

    rows = []
    total_outstanding = 0
    total_value = 0
    not_due = 0
    overdue = 0

    for row in results:
        # Considera "em falta" si la factura no está pagada
        em_falta = row.total_amount if row.status != "paid" else 0
        total_value += row.total_amount
        total_outstanding += em_falta
        if row.status == "paid":
            not_due += 0
        else:
            overdue += em_falta

        rows.append({
            "client_name": row.client_name,
            "document_type": "Factura",
            "invoice_number": row.invoice_number,
            "due_date": row.due_date.isoformat() if row.due_date else "",
            "outstanding": em_falta,
            "total": row.total_amount
        })

    return jsonify({
        "rows": rows,
        "totals": {
            "outstanding": total_outstanding,
            "total": total_value,
            "not_due": not_due,
            "overdue": overdue
        }
    })
