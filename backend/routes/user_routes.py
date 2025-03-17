from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import User, Role, Permission, AuditLog, log_action
from routes.utils import require_permission
from sqlalchemy.exc import IntegrityError

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def user_profile():
    """Obtiene información del perfil del usuario actual."""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    log_action(user_id, 'view_profile', 'User', user_id)
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role.name,
        'is_active': user.is_active,
        'two_factor_enabled': user.two_factor_enabled,
        'name': user.name,
        'second_name': user.second_name,
        'last_name': user.last_name,
        'phone_number': user.phone_number
    }), 200

@user_bp.route('', methods=['GET'])
@jwt_required()
@require_permission('view_users')
def get_users():
    """Obtiene una lista paginada de todos los usuarios."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    users = User.query.paginate(page=page, per_page=per_page)
    
    log_action(get_jwt_identity(), 'list_users', 'User', None)
    
    return jsonify({
        'users': [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role.name,
            'is_active': user.is_active,
            'name': f"{user.name} {user.last_name}"
        } for user in users.items],
        'total': users.total,
        'page': users.page,
        'per_page': users.per_page
    }), 200

@user_bp.route('', methods=['POST'])
@jwt_required()
@require_permission('create_user')
def create_user():
    """Crea un nuevo usuario con validación avanzada."""
    data = request.get_json()
    required_fields = ['username', 'email', 'password', 'role_id']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    
    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return jsonify({'error': 'El usuario o email ya existen'}), 409
    
    try:
        role = Role.query.get_or_404(data['role_id'])
        current_user_id = get_jwt_identity()
        
        new_user = User(
            username=data['username'],
            email=data['email'],
            role_id=role.id,
            name=data.get('name', ''),
            last_name=data.get('last_name', ''),
            phone_number=data.get('phone_number')
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        log_action(current_user_id, 'create_user', 'User', new_user.id)
        
        return jsonify({
            'message': 'Usuario creado exitosamente',
            'user_id': new_user.id
        }), 201
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Error de integridad en la base de datos', 'details': str(e)}), 400

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@require_permission('update_user')
def update_user(user_id):
    """Actualiza un usuario existente con validación de seguridad."""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    # Validar que no se pueda modificar el propio rol
    if str(user_id) == str(current_user_id) and 'role_id' in data:
        return jsonify({'error': 'No puedes modificar tu propio rol'}), 403
    
    # Actualizar campos permitidos
    allowed_fields = ['email', 'name', 'second_name', 'last_name', 'phone_number', 'is_active', 'role_id']
    updates = {k: v for k, v in data.items() if k in allowed_fields}
    
    # Validar rol
    if 'role_id' in updates:
        role = Role.query.get(updates['role_id'])
        if not role:
            return jsonify({'error': 'Rol no válido'}), 400
    
    try:
        for key, value in updates.items():
            setattr(user, key, value)
        
        db.session.commit()
        log_action(current_user_id, 'update_user', 'User', user_id)
        
        return jsonify({'message': 'Usuario actualizado correctamente'}), 200
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Conflicto de datos, verifique la información'}), 409

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@require_permission('delete_user')
def delete_user(user_id):
    """Elimina un usuario con validación de seguridad."""
    if user_id == get_jwt_identity():
        return jsonify({'error': 'No puedes eliminarte a ti mismo'}), 403
    
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        log_action(get_jwt_identity(), 'delete_user', 'User', user_id)
        
        return jsonify({'message': 'Usuario eliminado correctamente'}), 200
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'No se puede eliminar el usuario debido a dependencias'}), 409

@user_bp.route('/permissions', methods=['GET'])
@jwt_required()
def get_user_permissions():
    """Obtiene los permisos del usuario actual."""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        'permissions': [permission.name for permission in user.role.permissions]
    }), 200

@user_bp.route('/<int:user_id>/activate', methods=['PATCH'])
@jwt_required()
@require_permission('manage_users')
def toggle_user_status(user_id):
    """Activa/desactiva un usuario (solo para administradores)."""
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    action = 'activate_user' if user.is_active else 'deactivate_user'
    log_action(get_jwt_identity(), action, 'User', user_id)
    
    return jsonify({
        'message': f'Usuario {"activado" if user.is_active else "desactivado"} correctamente'
    }), 200

    # Añadir nueva ruta de administración
@user_bp.route('/admin', methods=['GET'])
@jwt_required()
@require_permission('admin_access')
def admin_panel():
    """Panel de administración del sistema"""
    admin_user = User.query.get(get_jwt_identity())
    
    log_action(admin_user.id, 'access_admin_panel', 'System', None)
    
    return jsonify({
        'message': 'Bienvenido al panel de administración',
        'stats': {
            'total_users': User.query.count(),
            'active_users': User.query.filter_by(is_active=True).count()
        }
    }), 200