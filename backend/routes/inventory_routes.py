from flask import Blueprint, jsonify, request
from models.inventory import Inventory
from models.product import Product
from extensions import db
from datetime import datetime

inventory_bp = Blueprint('inventory_bp', __name__)

@inventory_bp.route('/movement', methods=['POST'])
def create_inventory_movement():
    try:
        data = request.json
        if not all(key in data for key in ('product_id', 'movement_type', 'quantity')):
            return jsonify({'error': 'Missing required fields'}), 400

        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        quantity = int(data['quantity'])
        if data['movement_type'] == 'entrada':
            product.stock += quantity
        elif data['movement_type'] == 'salida':
            if product.stock < quantity:
                return jsonify({'error': 'Insufficient stock'}), 400
            product.stock -= quantity
        elif data['movement_type'] == 'ajuste':
            product.stock = quantity
        elif data['movement_type'] == 'transferencia':
            if product.stock < quantity:
                return jsonify({'error': 'Insufficient stock for transfer'}), 400
            product.stock -= quantity
        else:
            return jsonify({'error': 'Invalid movement type'}), 400

        movement = Inventory(
            product_id=product.id,
            movement_type=data['movement_type'],
            quantity=quantity,
            reason=data.get('reason', ''),
            location=data.get('location', ''),
            target_location=data.get('target_location', '')
        )
        db.session.add(movement)
        db.session.commit()

        return jsonify(movement.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/history/<int:product_id>', methods=['GET'])
def get_inventory_history(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        movements = Inventory.query.filter_by(product_id=product_id).all()
        return jsonify([movement.to_dict() for movement in movements]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/transfer', methods=['POST'])
def transfer_stock():
    try:
        data = request.json
        if not all(key in data for key in ('product_id', 'quantity', 'source', 'target')):
            return jsonify({'error': 'Missing required fields'}), 400

        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        if product.stock < data['quantity']:
            return jsonify({'error': 'Insufficient stock for transfer'}), 400

        product.stock -= data['quantity']
        movement = Inventory(
            product_id=product.id,
            movement_type='transferencia',
            quantity=data['quantity'],
            location=data['source'],
            target_location=data['target']
        )
        db.session.add(movement)
        db.session.commit()
        return jsonify({'message': 'Transfer completed successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    