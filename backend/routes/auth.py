from datetime import timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager
)
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db
from models.user import User, Role
from utils.api_helpers import validate_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def handle_login():
    try:
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Email y contraseña requeridos"}), 400

        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({"error": "Credenciales inválidas"}), 401

        access_token = create_access_token(identity={
            "id": user.id,
            "email": user.email,
            "role": user.role.name
        }, expires_delta=timedelta(hours=1))

        return jsonify({
            "message": "Login exitoso",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role.name
            }
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500

@auth_bp.route('/register', methods=['POST'])
def handle_registration():
    try:
        data = request.get_json()
        required_fields = ['email', 'password']
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        if not validate_email(data['email']):
            return jsonify({"error": "Formato de email inválido"}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "El email ya está registrado"}), 409

        default_role = Role.query.filter_by(name='Guest').first()
        if not default_role:
            return jsonify({"error": "Error de configuración del sistema"}), 500

        new_user = User(
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            role_id=default_role.id,
            name=data.get('name'),
            phone=data.get('phone')
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "Usuario registrado exitosamente",
            "userId": new_user.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al registrar usuario: {str(e)}"}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    try:
        claims = get_jwt_identity()
        user = User.query.get(claims['id'])
        
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "phone": user.phone,
            "role": user.role.name,
            "created_at": user.created_at.isoformat()
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error al obtener perfil: {str(e)}"}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh_auth_token():
    try:
        claims = get_jwt_identity()
        new_token = create_access_token(identity=claims)
        return jsonify({"access_token": new_token}), 200
    except Exception as e:
        return jsonify({"error": f"Error al refrescar token: {str(e)}"}), 500

@auth_bp.route('/password-reset', methods=['POST'])
def initiate_password_reset():
    # Implementación de recuperación de contraseña
    pass

@auth_bp.route('/validate-reset-token', methods=['POST'])
def validate_reset_token():
    # Validación de token de recuperación
    pass

@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
def verify_token():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    return jsonify(user.to_dict()), 200
