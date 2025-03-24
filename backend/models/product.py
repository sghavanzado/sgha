from extensions import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'  
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    expiration_date = db.Column(db.Date, nullable=True)
    image_url = db.Column(db.String(255), default='')
    attributes = db.Column(db.JSON, default={})
    stock = db.Column(db.Integer, default=0)
    location = db.Column(db.String(100), default='')

    # Relación con Inventory
    inventory_movements = db.relationship('Inventory', back_populates='product')

    def to_dict(self):
        return {
            'id': self.id,
            'sku': self.sku,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'unit': self.unit,
            'category': self.category,
            'expiration_date': self.expiration_date.strftime('%Y-%m-%d') if self.expiration_date else None,
            'image_url': self.image_url,
            'attributes': self.attributes,
            'stock': self.stock,
            'location': self.location
        }

class ProductPriceHistory(db.Model):
    __tablename__ = 'product_price_history'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  
    old_price = db.Column(db.Float, nullable=False)
    new_price = db.Column(db.Float, nullable=False)
    change_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con Product
    product = db.relationship('Product', back_populates='price_history')

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'old_price': self.old_price,
            'new_price': self.new_price,
            'change_date': self.change_date.isoformat(),
        }

# Añadir relación en Product
Product.price_history = db.relationship(
    'ProductPriceHistory', 
    back_populates='product',
    cascade='all, delete-orphan'
)