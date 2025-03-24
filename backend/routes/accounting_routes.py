from flask import Blueprint, request, jsonify
from extensions import db
from models.accounting import (
    AccountPlan, AccountingEntry, SupportingDocument, Employee,
    InventoryItem, TaxConfig, CostCenter, Project, ChangeHistory
)
from models.supplier import Supplier  # Updated import for Supplier
from models.client import Client  # Ensure Client is imported from models/client.py
from flask_jwt_extended import jwt_required

accounting_bp = Blueprint('accounting', __name__)

# Rutas para Plano de Contas
@accounting_bp.route('/account_plans', methods=['GET'])
@jwt_required()
def get_account_plans():
    account_plans = AccountPlan.query.all()
    return jsonify([account_plan.to_dict() for account_plan in account_plans])

@accounting_bp.route('/account_plans', methods=['POST'])
@jwt_required()
def create_account_plan():
    data = request.get_json()
    account_plan = AccountPlan(**data)
    db.session.add(account_plan)
    db.session.commit()
    return jsonify(account_plan.to_dict()), 201

# Rutas para Lançamentos Contábeis
@accounting_bp.route('/accounting_entries', methods=['GET'])
@jwt_required()
def get_accounting_entries():
    accounting_entries = AccountingEntry.query.all()
    return jsonify([entry.to_dict() for entry in accounting_entries])

@accounting_bp.route('/accounting_entries', methods=['POST'])
@jwt_required()
def create_accounting_entry():
    data = request.get_json()
    accounting_entry = AccountingEntry(**data)
    db.session.add(accounting_entry)
    db.session.commit()
    return jsonify(accounting_entry.to_dict()), 201

# Rutas para Documentos Suporte
@accounting_bp.route('/supporting_documents', methods=['GET'])
@jwt_required()
def get_supporting_documents():
    supporting_documents = SupportingDocument.query.all()
    return jsonify([document.to_dict() for document in supporting_documents])

@accounting_bp.route('/supporting_documents', methods=['POST'])
@jwt_required()
def create_supporting_document():
    data = request.get_json()
    supporting_document = SupportingDocument(**data)
    db.session.add(supporting_document)
    db.session.commit()
    return jsonify(supporting_document.to_dict()), 201

# Rutas para Clientes
@accounting_bp.route('/clients', methods=['GET'])
@jwt_required()
def get_clients():
    clients = Client.query.all()
    return jsonify([client.to_dict() for client in clients])

@accounting_bp.route('/clients', methods=['POST'])
@jwt_required()
def create_client():
    data = request.get_json()
    client = Client(**data)
    db.session.add(client)
    db.session.commit()
    return jsonify(client.to_dict()), 201

# Rutas para Fornecedores
@accounting_bp.route('/suppliers', methods=['GET'])
@jwt_required()
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([supplier.to_dict() for supplier in suppliers])

@accounting_bp.route('/suppliers', methods=['POST'])
@jwt_required()
def create_supplier():
    data = request.get_json()
    supplier = Supplier(**data)
    db.session.add(supplier)
    db.session.commit()
    return jsonify(supplier.to_dict()), 201

# Rutas para Funcionários
@accounting_bp.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
    employees = Employee.query.all()
    return jsonify([employee.to_dict() for employee in employees])

@accounting_bp.route('/employees', methods=['POST'])
@jwt_required()
def create_employee():
    data = request.get_json()
    employee = Employee(**data)
    db.session.add(employee)
    db.session.commit()
    return jsonify(employee.to_dict()), 201

# Rutas para Inventário/Estoque
@accounting_bp.route('/inventory_items', methods=['GET'])
@jwt_required()
def get_inventory_items():
    inventory_items = InventoryItem.query.all()
    return jsonify([item.to_dict() for item in inventory_items])

@accounting_bp.route('/inventory_items', methods=['POST'])
@jwt_required()
def create_inventory_item():
    data = request.get_json()
    inventory_item = InventoryItem(**data)
    db.session.add(inventory_item)
    db.session.commit()
    return jsonify(inventory_item.to_dict()), 201

# Rutas para Configurações Fiscais
@accounting_bp.route('/tax_configs', methods=['GET'])
@jwt_required()
def get_tax_configs():
    tax_configs = TaxConfig.query.all()
    return jsonify([tax_config.to_dict() for tax_config in tax_configs])

@accounting_bp.route('/tax_configs', methods=['POST'])
@jwt_required()
def create_tax_config():
    data = request.get_json()
    tax_config = TaxConfig(**data)
    db.session.add(tax_config)
    db.session.commit()
    return jsonify(tax_config.to_dict()), 201

# Rutas para Usuários do Sistema
@accounting_bp.route('/sys_users', methods=['GET'])
@jwt_required()
def get_sys_users():
    sys_users = SystemUser.query.all()
    return jsonify([sys_user.to_dict() for sys_user in sys_users])

@accounting_bp.route('/sys_users', methods=['POST'])
@jwt_required()
def create_sys_user():
    data = request.get_json()
    sys_user = SystemUser(**data)
    db.session.add(sys_user)
    db.session.commit()
    return jsonify(sys_user.to_dict()), 201

# Rutas para Centros de Custo
@accounting_bp.route('/cost_centers', methods=['GET'])
@jwt_required()
def get_cost_centers():
    cost_centers = CostCenter.query.all()
    return jsonify([cost_center.to_dict() for cost_center in cost_centers])

@accounting_bp.route('/cost_centers', methods=['POST'])
@jwt_required()
def create_cost_center():
    data = request.get_json()
    cost_center = CostCenter(**data)
    db.session.add(cost_center)
    db.session.commit()
    return jsonify(cost_center.to_dict()), 201

# Rutas para Projetos
@accounting_bp.route('/projects', methods=['GET'])
@jwt_required()
def get_projects():
    projects = Project.query.all()
    return jsonify([project.to_dict() for project in projects])

@accounting_bp.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    data = request.get_json()
    project = Project(**data)
    db.session.add(project)
    db.session.commit()
    return jsonify(project.to_dict()), 201

# Rutas para Histórico de Alterações
@accounting_bp.route('/change_histories', methods=['GET'])
@jwt_required()
def get_change_histories():
    change_histories = ChangeHistory.query.all()
    return jsonify([change_history.to_dict() for change_history in change_histories])

@accounting_bp.route('/change_histories', methods=['POST'])
@jwt_required()
def create_change_history():
    data = request.get_json()
    change_history = ChangeHistory(**data)
    db.session.add(change_history)
    db.session.commit()
    return jsonify(change_history.to_dict()), 201

from flask import Blueprint, jsonify, request
from extensions import db
from models.accounting import AccountingEntry
from flask_jwt_extended import jwt_required

accounting_bp = Blueprint('accounting', __name__, url_prefix='/accounting')

@accounting_bp.route('/entries', methods=['GET'])
@jwt_required()
def get_entries():
    """Get all accounting entries."""
    entries = AccountingEntry.query.all()
    return jsonify([entry.to_dict() for entry in entries]), 200

@accounting_bp.route('/entries', methods=['POST'])
@jwt_required()
def create_entry():
    """Create a new accounting entry."""
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    entry = AccountingEntry(**data)
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.to_dict()), 201

@accounting_bp.route('/entries/<int:entry_id>', methods=['PUT'])
@jwt_required()
def update_entry(entry_id):
    """Update an existing accounting entry."""
    entry = AccountingEntry.query.get(entry_id)
    if not entry:
        return jsonify({'message': 'Entry not found'}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(entry, key, value)

    db.session.commit()
    return jsonify(entry.to_dict()), 200

@accounting_bp.route('/entries/<int:entry_id>', methods=['DELETE'])
@jwt_required()
def delete_entry(entry_id):
    """Delete an accounting entry."""
    entry = AccountingEntry.query.get(entry_id)
    if not entry:
        return jsonify({'message': 'Entry not found'}), 404

    db.session.delete(entry)
    db.session.commit()
    return jsonify({'message': 'Entry deleted'}), 200
