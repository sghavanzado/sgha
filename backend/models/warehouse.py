from extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Warehouse:
    __tablename__ = 'warehouses'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    location = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def get_all_warehouses():
        query = """SELECT * FROM warehouses"""
        return [dict(row) for row in db.session.execute(query).fetchall()]
