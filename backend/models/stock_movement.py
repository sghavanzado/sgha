from extensions import db
from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class StockMovement:
    __tablename__ = 'stock_movements'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'), nullable=False)
    quantity = Column(Float, nullable=False)
    movement_type = Column(String(10), nullable=False)  # "IN" o "OUT"
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="movements")
    warehouse = relationship("Warehouse", back_populates="movements")

    @staticmethod
    def get_movements_by_warehouse(warehouse_id):
        query = """SELECT * FROM stock_movements WHERE warehouse_id = :warehouse_id"""
        return [dict(row) for row in db.session.execute(query, {'warehouse_id': warehouse_id}).fetchall()]

    @staticmethod
    def transfer_stock(source_warehouse_id, target_warehouse_id, product_id, quantity):
        # Verificar stock disponible en el almacén origen
        stock_query = """SELECT SUM(quantity) AS stock
                         FROM stock_movements
                         WHERE warehouse_id = :source_warehouse_id AND product_id = :product_id"""
        stock = db.ession.execute(stock_query, {
            'source_warehouse_id': source_warehouse_id,
            'product_id': product_id
        }).fetchone()['stock']

        if stock < quantity:
            raise ValueError("Stock insuficiente en el almacén origen.")

        # Registrar salida en el almacén origen
        db.session.execute(
            """INSERT INTO stock_movements (product_id, warehouse_id, quantity, movement_type, created_at)
               VALUES (:product_id, :warehouse_id, :quantity, 'OUT', :created_at)""",
            {
                'product_id': product_id,
                'warehouse_id': source_warehouse_id,
                'quantity': -quantity,
                'created_at': datetime.utcnow()
            }
        )

        # Registrar entrada en el almacén destino
        db.session.execute(
            """INSERT INTO stock_movements (product_id, warehouse_id, quantity, movement_type, created_at)
               VALUES (:product_id, :warehouse_id, :quantity, 'IN', :created_at)""",
            {
                'product_id': product_id,
                'warehouse_id': target_warehouse_id,
                'quantity': quantity,
                'created_at': datetime.utcnow()
            }
        )

        db.session.commit()
