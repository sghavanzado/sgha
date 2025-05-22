from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.client import Client
from models.receipt import Receipt
from models.invoice import Invoice
from datetime import datetime

payments_made_report_bp = Blueprint('payments_made_report', __name__)

@payments_made_report_bp.route('/api/payments-made-report', methods=['GET'])
@jwt_required()
def payments_made_report():
    client_id = request.args.get('client_id')
    date_str = request.args.get('date')
    try:
        report_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else datetime.utcnow().date()
    except Exception:
        report_date = datetime.utcnow().date()

    query = db.session.query(
        Client.name.label('client_name'),
        Receipt.receipt_number,
        Invoice.invoice_number,
        Invoice.due_date,
        Invoice.total_amount,
        Invoice.status
    ).join(Receipt, Receipt.client_id == Client.id)\
     .join(Invoice, Invoice.client_id == Client.id)\
     .filter(Receipt.issue_date <= report_date)

    if client_id and client_id != "all":
        query = query.filter(Client.id == int(client_id))

    results = query.all()

    rows = []
    total_paid = 0
    total_due = 0
    not_due = 0
    overdue = 0

    for row in results:
        # Simulación: si la factura está pagada, se considera "Pagamentos Efectuados"
        em_falta = 0 if row.status == "paid" else row.total_amount
        total_paid += row.total_amount if row.status == "paid" else 0
        total_due += em_falta
        if row.status == "paid":
            not_due += row.total_amount
        else:
            overdue += em_falta

        rows.append({
            "client_name": row.client_name,
            "document_type": "Recibo",
            "receipt_number": row.receipt_number,
            "invoice_number": row.invoice_number,
            "due_date": row.due_date.isoformat() if row.due_date else "",
            "outstanding": em_falta,
            "total": row.total_amount
        })

    return jsonify({
        "rows": rows,
        "totals": {
            "paid": total_paid,
            "due": total_due,
            "not_due": not_due,
            "overdue": overdue,
            "total": total_paid + total_due
        }
    })
