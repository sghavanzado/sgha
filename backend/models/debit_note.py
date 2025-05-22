from extensions import db
from datetime import datetime

class DebitNote(db.Model):
    __tablename__ = 'debit_notes'

    id = db.Column(db.Integer, primary_key=True)
    debit_note_number = db.Column(db.String(50), nullable=False, unique=True)
    issue_date = db.Column(db.DateTime, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

    # Relationship with Client
    client = db.relationship('Client', backref=db.backref('debit_notes', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'debit_note_number': self.debit_note_number,
            'issue_date': self.issue_date.isoformat(),
            'client_id': self.client_id,
            'total_amount': self.total_amount,
            'client': self.client.to_dict() if self.client else None,
        }
