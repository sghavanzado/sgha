from extensions import db

class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.JSON, nullable=False)  # {"email": "example@example.com", "phone": "123456789"}
    payment_terms = db.Column(db.String(100), nullable=True)
    delivery_times = db.Column(db.String(100), nullable=True)
    active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact_info': self.contact_info,
            'payment_terms': self.payment_terms,
            'delivery_times': self.delivery_times,
            'active': self.active,
        }
