from flask import Blueprint, jsonify, request
from extensions import db
from models.unit import UnitOfMeasure
from flask_jwt_extended import jwt_required

unit_bp = Blueprint('units', __name__, url_prefix='/units')

@unit_bp.route('/', methods=['GET'])
@jwt_required()
def get_units():
    """Get all units of measure."""
    units = UnitOfMeasure.query.all()
    return jsonify([unit.to_dict() for unit in units]), 200
