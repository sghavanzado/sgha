from extensions import db

class UnitOfMeasure(db.Model):
    __tablename__ = 'units_of_measure'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    abbreviation = db.Column(db.String(10), nullable=False, unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'abbreviation': self.abbreviation,
        }
