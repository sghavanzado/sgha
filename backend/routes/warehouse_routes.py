from flask import Blueprint, jsonify, request
from models.warehouse import Warehouse
from models.stock_movement import StockMovement

warehouse_bp = Blueprint('warehouse', __name__)

@warehouse_bp.route('/', methods=['GET'])
def get_all_warehouses():
    warehouses = Warehouse.get_all_warehouses()
    return jsonify(warehouses), 200

@warehouse_bp.route('/<int:warehouse_id>/movements', methods=['GET'])
def get_movements(warehouse_id):
    movements = StockMovement.get_movements_by_warehouse(warehouse_id)
    return jsonify(movements), 200

@warehouse_bp.route('/transfer', methods=['POST'])
def transfer_stock():
    data = request.json
    source_warehouse = data['source_warehouse']
    target_warehouse = data['target_warehouse']
    product_id = data['product_id']
    quantity = data['quantity']

    try:
        StockMovement.transfer_stock(source_warehouse, target_warehouse, product_id, quantity)
        return jsonify({'message': 'Transferencia realizada con éxito'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
