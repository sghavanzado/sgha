from extensions import db
from datetime import datetime

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(50), nullable=False)  # invoice, order, etc.
    reference = db.Column(db.String(100), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    movements = db.relationship('Inventory', backref='document', lazy=True)  # Relación ajustada

    def to_dict(self):
        return {
            'id': self.id,
            'document_type': self.document_type,
            'reference': self.reference,
            'timestamp': self.timestamp.isoformat(),
            'movements': [movement.to_dict() for movement in self.movements],
        }
