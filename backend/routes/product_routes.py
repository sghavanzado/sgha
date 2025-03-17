from flask import Blueprint, jsonify, request
from models.product import Product
from extensions import db
from datetime import datetime

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('', methods=['POST'])
def create_product():
    try:
        data = request.json
        if not all(key in data for key in ('sku', 'name', 'price', 'unit', 'category')):
            return jsonify({'error': 'Missing required fields'}), 400

        product = Product(
            sku=data['sku'],
            name=data['name'],
            description=data.get('description', ''),
            price=float(data['price']),
            unit=data['unit'],
            category=data['category'],
            expiration_date=datetime.strptime(data['expiration_date'], '%Y-%m-%d') if data.get('expiration_date') else None,
            image_url=data.get('image_url', ''),
            attributes=data.get('attributes', {}),
            stock=data.get('stock', 0),
            location=data.get('location', '')
        )
        db.session.add(product)
        db.session.commit()

        return jsonify(product.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@product_bp.route('', methods=['GET', 'OPTIONS'])
def list_products():
    try:
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@product_bp.route('<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(product.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@product_bp.route('<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        data = request.json
        product.sku = data.get('sku', product.sku)
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = float(data.get('price', product.price))
        product.unit = data.get('unit', product.unit)
        product.category = data.get('category', product.category)
        product.expiration_date = datetime.strptime(data['expiration_date'], '%Y-%m-%d') if data.get('expiration_date') else product.expiration_date
        product.image_url = data.get('image_url', product.image_url)
        product.attributes = data.get('attributes', product.attributes)
        product.stock = data.get('stock', product.stock)
        product.location = data.get('location', product.location)

        db.session.commit()
        return jsonify(product.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@product_bp.route('<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
