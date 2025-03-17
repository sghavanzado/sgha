from extensions import db
from datetime import datetime
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import validates

class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)  
    movement_type = db.Column(db.String(20), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    reason = db.Column(db.String(255))
    location = db.Column(db.String(255))
    target_location = db.Column(db.String(255))
    document_id = db.Column(db.Integer, ForeignKey('documents.id')) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones actualizadas
    document = db.relationship('Document', backref='inventory_movements', lazy='joined')
    product = db.relationship('Product', back_populates='inventory_movements')

    __table_args__ = (
        CheckConstraint(
            "movement_type IN ('entry', 'exit', 'adjustment', 'transfer')",
            name='check_valid_movement_type'
        ),
        CheckConstraint('quantity > 0', name='check_positive_quantity'),
        db.Index('ix_movement_timestamp', 'movement_type', 'timestamp'),
    )

    @validates('movement_type')
    def validate_movement_type(self, key, movement_type):
        valid_types = ['entry', 'exit', 'adjustment', 'transfer']
        if movement_type not in valid_types:
            raise ValueError(f"Tipo de movimiento inválido: {movement_type}")
        return movement_type

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'movement_type': self.movement_type,
            'quantity': self.quantity,
            'timestamp': self.timestamp.isoformat(),
            'reason': self.reason,
            'location': self.location,
            'target_location': self.target_location,
            'document_id': self.document_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<Inventory {self.movement_type} {self.quantity} units>'