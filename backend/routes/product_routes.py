import logging  # Add this import
from flask import Blueprint, jsonify, request
from extensions import db
from models.product import Product
from sqlalchemy.exc import IntegrityError
from datetime import datetime

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('', methods=['POST'])
def create_product():
    """Create a new product or multiple products."""
    try:
        data = request.get_json()
        if not data:
            logging.error("No data provided in request")
            return jsonify({'message': 'No data provided'}), 400
    except Exception as e:
        logging.error(f"Invalid JSON format: {str(e)}")
        return jsonify({'message': 'Invalid JSON format'}), 400

    if isinstance(data, list):  # Handle bulk creation
        products = []
        for product_data in data:
            if not isinstance(product_data, dict):  # Ensure each item is a dictionary
                logging.error(f"Invalid data format for bulk creation: {product_data}")
                return jsonify({'message': 'Invalid data format for bulk creation'}), 400
            if Product.query.filter_by(sku=product_data.get('sku')).first():  # Check for duplicate SKU
                logging.error(f"Duplicate SKU detected: {product_data.get('sku')}")
                return jsonify({'message': f"Duplicate SKU: {product_data.get('sku')}"}), 400
            try:
                product = Product(
                    sku=product_data['sku'],
                    name=product_data['name'],
                    description=product_data.get('description', ''),
                    price=float(product_data['price']),
                    unit=product_data['unit'],
                    category=product_data['category'],
                    expiration_date=datetime.strptime(product_data['expiration_date'], '%Y-%m-%d') if product_data.get('expiration_date') else None,
                    image_url=product_data.get('image_url', ''),
                    attributes=product_data.get('attributes', {}),
                    stock=product_data.get('stock', 0),
                    location=product_data.get('location', '')
                )
                db.session.add(product)
                products.append(product.to_dict())
            except Exception as e:
                db.session.rollback()
                logging.error(f"Error creating product: {str(e)}")
                return jsonify({'message': f"Error creating product: {str(e)}"}), 400
        db.session.commit()
        return jsonify({'message': 'Products created successfully', 'products': products}), 201

    elif isinstance(data, dict):  # Handle single creation
        if Product.query.filter_by(sku=data.get('sku')).first():  # Check for duplicate SKU
            logging.error(f"Duplicate SKU detected: {data.get('sku')}")
            return jsonify({'message': f"Duplicate SKU: {data.get('sku')}"}), 400  # Fixed closing parenthesis
        try:
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
            logging.error(f"Error creating product: {str(e)}")
            return jsonify({'message': f"Error creating product: {str(e)}"}), 400

    logging.error(f"Invalid data format: {data}")
    return jsonify({'message': 'Invalid data format'}), 400

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
