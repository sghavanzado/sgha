from extensions import db

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    nif = db.Column(db.String(20), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    contact_first_name = db.Column(db.String(100), nullable=True)
    contact_last_name = db.Column(db.String(100), nullable=True)
    contact_email = db.Column(db.String(100), nullable=True)
    contact_phone_number = db.Column(db.String(20), nullable=True)
    payment_terms = db.Column(db.String(100), nullable=True)
    bank_name = db.Column(db.String(100), nullable=True)
    iban_number = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'nif': self.nif,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'phone': self.phone,
            'email': self.email,
            'contact_first_name': self.contact_first_name,
            'contact_last_name': self.contact_last_name,
            'contact_email': self.contact_email,
            'contact_phone_number': self.contact_phone_number,
            'payment_terms': self.payment_terms,
            'bank_name': self.bank_name,
            'iban_number': self.iban_number,
        }
