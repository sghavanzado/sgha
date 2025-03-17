from extensions import db
from datetime import datetime
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False, index=True)
    reference = db.Column(db.String(100), unique=True, nullable=False, index=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint(
            "type IN ('invoice', 'order', 'transfer', 'adjustment')",
            name='check_valid_document_type'
        ),
        db.Index('ix_document_type_date', 'type', 'date'),
    )

    @validates('type')
    def validate_type(self, key, document_type):
        valid_types = ['invoice', 'order', 'transfer', 'adjustment']
        if document_type not in valid_types:
            raise ValueError(f"Tipo de documento inválido: {document_type}")
        return document_type

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "reference": self.reference,
            "date": self.date.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "movements_count": self.inventory_movements.count()
        }

    def __repr__(self):
        return f'<Document {self.reference} ({self.type})>'