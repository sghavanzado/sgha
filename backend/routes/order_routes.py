from flask import Blueprint, jsonify, request
from models.order import Order
from models.provider import Provider
from extensions import db

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('', methods=['POST'])
def create_order():
    try:
        data = request.json
        if not all(key in data for key in ('provider_id', 'total_amount', 'status')):
            return jsonify({'error': 'Missing required fields'}), 400

        provider = Provider.query.get(data['provider_id'])
        if not provider:
            return jsonify({'error': 'Provider not found'}), 404

        order = Order(
            provider_id=data['provider_id'],
            total_amount=float(data['total_amount']),
            status=data['status']
        )
        db.session.add(order)
        db.session.commit()
        return jsonify(order.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@order_bp.route('', methods=['GET'])
def list_orders():
    try:
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@order_bp.route('/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    try:
        data = request.json
        if 'status' not in data:
            return jsonify({'error': 'Missing status field'}), 400

        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        order.status = data['status']
        db.session.commit()
        return jsonify({'message': 'Order status updated successfully', 'order': order.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

