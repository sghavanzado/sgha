from flask import Blueprint, jsonify, request
from extensions import db
from models.location import Country, Province
from flask_jwt_extended import jwt_required

location_bp = Blueprint('locations', __name__, url_prefix='/locations')

@location_bp.route('/countries', methods=['GET'])
@jwt_required()
def get_countries():
    """Get all countries."""
    countries = Country.query.all()
    return jsonify([country.to_dict() for country in countries]), 200

@location_bp.route('/provinces', methods=['GET'])
@jwt_required()
def get_provinces():
    """Get all provinces."""
    provinces = Province.query.all()
    return jsonify([province.to_dict() for province in provinces]), 200

@location_bp.route('/provinces/<int:country_id>', methods=['GET'])
@jwt_required()
def get_provinces_by_country(country_id):
    """Get provinces by country."""
    provinces = Province.query.filter_by(country_id=country_id).all()
    return jsonify([province.to_dict() for province in provinces]), 200
