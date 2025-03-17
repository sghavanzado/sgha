from extensions import db

class PriceList(db.Model):
    __tablename__ = 'price_list'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Relación con los detalles de precios
    prices = db.relationship('PriceDetail', backref='price_list', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'prices': [price.to_dict() for price in self.prices],
        }


class PriceDetail(db.Model):
    __tablename__ = 'price_detail'
    id = db.Column(db.Integer, primary_key=True)
    price_list_id = db.Column(db.Integer, db.ForeignKey('price_list.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=True)  # Descuento en porcentaje
    volume_price = db.Column(db.JSON, nullable=True)  # {"5": 10.0, "10": 9.0}

    def to_dict(self):
        return {
            'id': self.id,
            'price_list_id': self.price_list_id,
            'product_id': self.product_id,
            'price': self.price,
            'discount': self.discount,
            'volume_price': self.volume_price,
        }
