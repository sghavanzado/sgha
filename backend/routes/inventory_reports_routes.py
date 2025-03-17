from flask import Blueprint, jsonify, request
from sqlalchemy import text
from datetime import datetime
from models.product import Product  # Cambiar de 'app.models.product' a 'models.product'
from extensions import db  # Usa 'db' en lugar de 'db_session'


inventory_reports_bp = Blueprint('inventory_reports', __name__)

@inventory_reports_bp.route('/top-selling-products', methods=['GET'])
def top_selling_products():
    try:
        # Consulta SQL para obtener los productos más vendidos
        query = text("""
            SELECT product_id, name, SUM(quantity) as total_sold
            FROM sales
            GROUP BY product_id, name
            ORDER BY total_sold DESC
            LIMIT 10;
        """)
        result = db.session.execute(query).fetchall()

        # Convertir los resultados en una lista de diccionarios
        products = [dict(row) for row in result]

        return jsonify(products), 200

    except Exception as e:
        # Manejo de errores
        return jsonify({"error": "Failed to fetch top-selling products", "details": str(e)}), 500

@inventory_reports_bp.route('/low-rotation-products', methods=['GET'])
def low_rotation_products():
    try:
        # Lógica para obtener productos de baja rotación
        query = text("""SELECT product_id, name, COUNT(*) as movements
               FROM inventory_movements
               GROUP BY product_id, name
               HAVING movements < 5
               ORDER BY movements ASC;
        """)
        result = db.session.execute(query).fetchall()

        return jsonify([dict(row) for row in result]), 200

    except Exception as e:
        # Manejo de errores
        return jsonify({"error": "Failed to fetch low-rotations products", "details": str(e)}), 500

@inventory_reports_bp.route('/inventory-value', methods=['GET'])
def inventory_value():
    try:
        # Lógica para calcular valor total del inventario
        query = text("""SELECT SUM(quantity * cost_price) as total_cost,
                      SUM(quantity * selling_price) as total_value
               FROM inventory;
        """)
        result = db.session.execute(query).fetchone()
        return jsonify(dict(result)), 200
    
    except Exception as e:
        # Manejo de errores
        return jsonify({"error": "Failed to fetch inventory-value", "details": str(e)}), 500
    

@inventory_reports_bp.route('/near-expiry-products', methods=['GET'])
def near_expiry_products():
     try:
         # Lógica para productos próximos a vencer
         days = int(request.args.get('days', 30))

         query = text("""SELECT product_id, name, expiry_date
               FROM inventory
               WHERE expiry_date <= NOW() + INTERVAL :days DAY;
         """)
         result = db.session.execute(query, {'days': days}).fetchall()

         return jsonify([dict(row) for row in result]), 200
     
     except Exception as e:
        # Manejo de errores
        return jsonify({"error": "Failed near-expiry-products", "details": str(e)}), 500
    

@inventory_reports_bp.route('/inventory-movements', methods=['GET'])
def inventory_movements():
    try:
         # Lógica para movimientos de inventario (entradas/salidas)
         start_date = request.args.get('start_date')
         end_date = request.args.get('end_date')
         movement_type = request.args.get('type')
         query = text("""SELECT * FROM inventory_movements
               WHERE movement_date BETWEEN :start_date AND :end_date
               AND (:movement_type IS NULL OR type = :movement_type);
         """)
         result = db.session.execute(query, {
         'start_date': start_date,
         'end_date': end_date,
         'movement_type': movement_type
         }).fetchall()
         return jsonify([dict(row) for row in result]), 200
    except Exception as e:
        # Manejo de errores
        return jsonify({"error": "Failed inventory-movements", "details": str(e)}), 500
