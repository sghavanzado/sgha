from extensions import db
from datetime import datetime

class TransportGuide(db.Model):
    __tablename__ = 'transport_guides'

    id = db.Column(db.Integer, primary_key=True)
    guide_number = db.Column(db.String(50), nullable=False, unique=True)
    issue_date = db.Column(db.DateTime, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

    # Detalhes do transporte
    vehicle_plate = db.Column(db.String(30), nullable=True)
    load_date = db.Column(db.DateTime, nullable=True)
    load_location = db.Column(db.String(255), nullable=True)
    load_address = db.Column(db.String(255), nullable=True)
    load_city = db.Column(db.String(100), nullable=True)
    load_postal_code = db.Column(db.String(20), nullable=True)
    delivery_location = db.Column(db.String(255), nullable=True)
    delivery_address = db.Column(db.String(255), nullable=True)
    delivery_city = db.Column(db.String(100), nullable=True)
    delivery_postal_code = db.Column(db.String(20), nullable=True)

    # Relationship with Client
    client = db.relationship('Client', backref=db.backref('transport_guides', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'guide_number': self.guide_number,
            'issue_date': self.issue_date.isoformat(),
            'client_id': self.client_id,
            'total_amount': self.total_amount,
            'vehicle_plate': self.vehicle_plate,
            'load_date': self.load_date.isoformat() if self.load_date else None,
            'load_location': self.load_location,
            'load_address': self.load_address,
            'load_city': self.load_city,
            'load_postal_code': self.load_postal_code,
            'delivery_location': self.delivery_location,
            'delivery_address': self.delivery_address,
            'delivery_city': self.delivery_city,
            'delivery_postal_code': self.delivery_postal_code,
            'client': self.client.to_dict() if self.client else None,
        }
