from extensions import db
from datetime import datetime

# Modelo de Factura
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    operation_date = db.Column(db.DateTime, nullable=True)
    seller_name = db.Column(db.String(100), nullable=False)
    seller_nif = db.Column(db.String(20), nullable=False)
    seller_address = db.Column(db.String(255), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    client_nif = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_of_measure = db.Column(db.String(50), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    taxable_amount = db.Column(db.Float, nullable=False)
    vat_rate = db.Column(db.Float, default=14.0, nullable=False)
    vat_amount = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    payment_due_date = db.Column(db.DateTime, nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)
    authorization_number = db.Column(db.String(50), nullable=True)
    legal_reference = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'issue_date': self.issue_date.isoformat(),
            'operation_date': self.operation_date.isoformat() if self.operation_date else None,
            'seller_name': self.seller_name,
            'seller_nif': self.seller_nif,
            'seller_address': self.seller_address,
            'client_name': self.client_name,
            'client_nif': self.client_nif,
            'description': self.description,
            'quantity': self.quantity,
            'unit_of_measure': self.unit_of_measure,
            'unit_price': self.unit_price,
            'taxable_amount': self.taxable_amount,
            'vat_rate': self.vat_rate,
            'vat_amount': self.vat_amount,
            'total_amount': self.total_amount,
            'payment_due_date': self.payment_due_date.isoformat() if self.payment_due_date else None,
            'payment_method': self.payment_method,
            'authorization_number': self.authorization_number,
            'legal_reference': self.legal_reference,
        }
