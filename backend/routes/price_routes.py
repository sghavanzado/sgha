from flask import Blueprint, jsonify, request
from models.price_list import PriceList, PriceDetail
from models.product import Product
from extensions import db

price_bp = Blueprint('price_bp', __name__)

@price_bp.route('', methods=['POST'])
def create_price_list():
    try:
        data = request.json
        if 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400

        price_list = PriceList(
            name=data['name'],
            description=data.get('description', '')
        )
        db.session.add(price_list)
        db.session.commit()
        return jsonify(price_list.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@price_bp.route('/<int:price_list_id>', methods=['POST'])
def add_price_detail(price_list_id):
    try:
        data = request.json
        if not all(key in data for key in ('product_id', 'price')):
            return jsonify({'error': 'Missing required fields'}), 400

        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        price_detail = PriceDetail(
            price_list_id=price_list_id,
            product_id=data['product_id'],
            price=data['price'],
            discount=data.get('discount'),
            volume_price=data.get('volume_price')
        )
        db.session.add(price_detail)
        db.session.commit()
        return jsonify(price_detail.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@price_bp.route('', methods=['GET'])
def list_price_lists():
    try:
        price_lists = PriceList.query.all()
        return jsonify([pl.to_dict() for pl in price_lists]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@price_bp.route('/<int:price_list_id>', methods=['GET'])
def get_price_list(price_list_id):
    try:
        price_list = PriceList.query.get(price_list_id)
        if not price_list:
            return jsonify({'error': 'Price list not found'}), 404
        return jsonify(price_list.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
