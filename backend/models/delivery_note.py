from extensions import db
from datetime import datetime

class DeliveryNote(db.Model):
    __tablename__ = 'delivery_notes'

    id = db.Column(db.Integer, primary_key=True)
    delivery_note_number = db.Column(db.String(50), nullable=False, unique=True)
    delivery_date = db.Column(db.DateTime, nullable=False)
    delivery_location = db.Column(db.String(255), nullable=True)
    issue_date = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.String(50), nullable=True)
    reference = db.Column(db.String(100), nullable=True)
    series = db.Column(db.String(50), nullable=True)
    currency = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    retention_percent = db.Column(db.Float, nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    items = db.Column(db.JSON, nullable=False)

    client = db.relationship('Client', backref=db.backref('delivery_notes', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'delivery_note_number': self.delivery_note_number,
            'delivery_date': self.delivery_date.isoformat(),
            'delivery_location': self.delivery_location,
            'issue_date': self.issue_date.isoformat(),
            'due_date': self.due_date,
            'reference': self.reference,
            'series': self.series,
            'currency': self.currency,
            'notes': self.notes,
            'retention_percent': self.retention_percent,
            'client_id': self.client_id,
            'items': self.items,
            'client': self.client.to_dict() if self.client else None,
        }
