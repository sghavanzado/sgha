from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from extensions import db

client_account_statement_report_bp = Blueprint('client_account_statement_report', __name__)

@client_account_statement_report_bp.route('/api/client-account-statement-report', methods=['GET'])
@jwt_required()
def client_account_statement_report():
    client_id = request.args.get('client_id')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    if not client_id:
        return jsonify({
            "rows": [],
            "client_selected": False
        })

    try:
        if date_from:
            date_from = date_from + " 00:00:00"
        if date_to:
            date_to = date_to + " 23:59:59"
    except Exception:
        date_from = None
        date_to = None

    # Suponiendo tabla invoices y recibos (payments) con client_id, issue_date, total, type
    # Unificamos facturas y recibos en el reporte
    invoice_query = db.session.query(
        db.literal_column("'Factura'").label('document_type'),
        db.literal_column('invoice_number').label('document_number'),
        db.literal_column('issue_date'),
        db.literal_column('total_amount').label('amount')
    ).select_from(db.text('invoices')).filter(db.literal_column('client_id') == client_id)
    if date_from:
        invoice_query = invoice_query.filter(db.literal_column('issue_date') >= date_from)
    if date_to:
        invoice_query = invoice_query.filter(db.literal_column('issue_date') <= date_to)

    receipt_query = db.session.query(
        db.literal_column("'Recibo'").label('document_type'),
        db.literal_column('receipt_number').label('document_number'),
        db.literal_column('issue_date'),
        (db.literal_column('total_amount') * -1).label('amount')
    ).select_from(db.text('receipts')).filter(db.literal_column('client_id') == client_id)
    if date_from:
        receipt_query = receipt_query.filter(db.literal_column('issue_date') >= date_from)
    if date_to:
        receipt_query = receipt_query.filter(db.literal_column('issue_date') <= date_to)

    # Unir ambos resultados y ordenar por fecha
    union_query = invoice_query.union_all(receipt_query).order_by(db.literal_column('issue_date'))

    results = union_query.all()

    rows = []
    for row in results:
        rows.append({
            "document_type": row.document_type,
            "document_number": row.document_number,
            "issue_date": row.issue_date,
            "amount": float(row.amount or 0),
        })

    return jsonify({
        "rows": rows,
        "client_selected": True
    })
