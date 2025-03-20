from extensions import db
from datetime import datetime
from models.user import User  # Import User model

# Modelo de Plano de Contas
class AccountPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_code = db.Column(db.String(20), unique=True, nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)  # Ativo, Passivo, Capital Próprio, Custos, Proveitos, etc.
    level = db.Column(db.Integer, nullable=False)
    parent_account_id = db.Column(db.Integer, db.ForeignKey('account_plan.id'), nullable=True)
    parent_account = db.relationship('AccountPlan', remote_side=[id], backref='sub_accounts')

    def to_dict(self):
        return {
            'id': self.id,
            'account_code': self.account_code,
            'account_name': self.account_name,
            'account_type': self.account_type,
            'level': self.level,
            'parent_account_id': self.parent_account_id,
        }

# Modelo de Lançamentos Contábeis
class AccountingEntry(db.Model):
    __tablename__ = 'accounting_entries'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    account_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'amount': self.amount,
            'date': self.date.isoformat(),
            'account_id': self.account_id,
        }

# Modelo de Documentos Suporte
class SupportingDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(50), nullable=False)  # fatura, recibo, nota de crédito, etc.
    document_number = db.Column(db.String(50), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False)
    supplier_client = db.Column(db.String(100), nullable=False)
    total_value = db.Column(db.Float, nullable=False)
    observations = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'document_type': self.document_type,
            'document_number': self.document_number,
            'issue_date': self.issue_date.isoformat(),
            'supplier_client': self.supplier_client,
            'total_value': self.total_value,
            'observations': self.observations,
        }

# Modelo de Clientes
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    nif = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.JSON, nullable=False)  # {"phone": "123456789", "email": "example@example.com"}
    contact_first_name = db.Column(db.String(100), nullable=False)
    contact_last_name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100), nullable=False)
    contact_phone_number = db.Column(db.String(20), nullable=False)
    payment_terms = db.Column(db.String(100), nullable=True)
    bank_name = db.Column(db.String(100), nullable=True)
    iban_number = db.Column(db.String(34), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'nif': self.nif,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'phone': self.phone,
            'contact_first_name': self.contact_first_name,
            'contact_last_name': self.contact_last_name,
            'contact_email': self.contact_email,
            'contact_phone_number': self.contact_phone_number,
            'payment_terms': self.payment_terms,
            'bank_name': self.bank_name,
            'iban_number': self.iban_number,
        }

# Modelo de Fornecedores
class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    nif = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.JSON, nullable=False)  # {"phone": "123456789", "email": "example@example.com"}
    contact_first_name = db.Column(db.String(100), nullable=False)
    contact_last_name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100), nullable=False)
    contact_phone_number = db.Column(db.String(20), nullable=False)
    bank_name = db.Column(db.String(100), nullable=True)
    iban_number = db.Column(db.String(34), nullable=True)
    payment_terms = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'nif': self.nif,
            'address': self.address,
            'phone': self.phone,
            'contact_first_name': self.contact_first_name,
            'contact_last_name': self.contact_last_name,
            'contact_email': self.contact_email,
            'contact_phone_number': self.contact_phone_number,
            'payment_terms': self.payment_terms,
            'bank_name': self.bank_name,
            'iban_number': self.iban_number,
        }

# Modelo de Funcionários
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    nif = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.JSON, nullable=False)  # {"phone": "123456789", "email": "example@example.com"}
    position = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'nif': self.nif,
            'address': self.address,
            'phone': self.phone,
            'position': self.position,
            'salary': self.salary,
        }

# Modelo de Inventário/Estoque
class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    barcode = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    cost_price = db.Column(db.Float, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'barcode': self.barcode,
            'category': self.category,
            'stock_quantity': self.stock_quantity,
            'cost_price': self.cost_price,
            'sale_price': self.sale_price,
        }

# Modelo de Configurações Fiscais
class TaxConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tax_description = db.Column(db.String(100), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    tax_type = db.Column(db.String(50), nullable=False)  # IVA, Imposto de Rendimento, etc.
    validity = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'tax_description': self.tax_description,
            'rate': self.rate,
            'tax_type': self.tax_type,
            'validity': self.validity.isoformat(),
        }

# Modelo de Centros de Custo
class CostCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    associated_code = db.Column(db.String(50), nullable=False)
    responsible_department = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'associated_code': self.associated_code,
            'responsible_department': self.responsible_department,
        }

# Modelo de Projetos
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'project_name': self.project_name,
            'description': self.description,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
        }

# Modelo de Histórico de Alterações
class ChangeHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    change_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    change_description = db.Column(db.Text, nullable=False)
    affected_table = db.Column(db.String(50), nullable=False)
    affected_record_id = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref=db.backref('change_histories', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'change_date': self.change_date.isoformat(),
            'user_id': self.user_id,
            'change_description': self.change_description,
            'affected_table': self.affected_table,
            'affected_record_id': self.affected_record_id,
        }
