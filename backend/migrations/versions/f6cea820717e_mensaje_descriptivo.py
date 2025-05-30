"""mensaje descriptivo

Revision ID: f6cea820717e
Revises: 
Create Date: 2025-05-16 22:58:29.415192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6cea820717e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account_plan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_code', sa.String(length=20), nullable=False),
    sa.Column('account_name', sa.String(length=100), nullable=False),
    sa.Column('account_type', sa.String(length=50), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('parent_account_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_account_id'], ['account_plan.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('account_code')
    )
    op.create_table('accounting_entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('nif', sa.String(length=20), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('state', sa.String(length=100), nullable=True),
    sa.Column('country', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('contact_first_name', sa.String(length=100), nullable=True),
    sa.Column('contact_last_name', sa.String(length=100), nullable=True),
    sa.Column('contact_email', sa.String(length=100), nullable=True),
    sa.Column('contact_phone_number', sa.String(length=20), nullable=True),
    sa.Column('payment_terms', sa.String(length=100), nullable=True),
    sa.Column('bank_name', sa.String(length=100), nullable=True),
    sa.Column('iban_number', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nif')
    )
    op.create_table('cost_center',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=False),
    sa.Column('associated_code', sa.String(length=50), nullable=False),
    sa.Column('responsible_department', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('countries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('code', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('name')
    )
    op.create_table('documents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('reference', sa.String(length=100), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.CheckConstraint("type IN ('invoice', 'order', 'transfer', 'adjustment')", name='check_valid_document_type'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.create_index('ix_document_type_date', ['type', 'date'], unique=False)
        batch_op.create_index(batch_op.f('ix_documents_reference'), ['reference'], unique=True)
        batch_op.create_index(batch_op.f('ix_documents_type'), ['type'], unique=False)

    op.create_table('employee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=100), nullable=False),
    sa.Column('nif', sa.String(length=20), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.JSON(), nullable=False),
    sa.Column('position', sa.String(length=50), nullable=False),
    sa.Column('salary', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inventory_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('barcode', sa.String(length=50), nullable=True),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('stock_quantity', sa.Integer(), nullable=False),
    sa.Column('cost_price', sa.Float(), nullable=False),
    sa.Column('sale_price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('price_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sku', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('unit', sa.String(length=20), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('expiration_date', sa.Date(), nullable=True),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.Column('attributes', sa.JSON(), nullable=True),
    sa.Column('stock', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sku')
    )
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('provider',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('contact_info', sa.JSON(), nullable=False),
    sa.Column('payment_terms', sa.String(length=100), nullable=True),
    sa.Column('delivery_times', sa.String(length=100), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('duration', sa.String(length=50), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('supplier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('nif', sa.String(length=20), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.JSON(), nullable=False),
    sa.Column('contact_first_name', sa.String(length=100), nullable=False),
    sa.Column('contact_last_name', sa.String(length=100), nullable=False),
    sa.Column('contact_email', sa.String(length=100), nullable=False),
    sa.Column('contact_phone_number', sa.String(length=20), nullable=False),
    sa.Column('bank_name', sa.String(length=100), nullable=True),
    sa.Column('iban_number', sa.String(length=34), nullable=True),
    sa.Column('payment_terms', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('suppliers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('nif', sa.String(length=20), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('contact_first_name', sa.String(length=100), nullable=True),
    sa.Column('contact_last_name', sa.String(length=100), nullable=True),
    sa.Column('contact_email', sa.String(length=100), nullable=True),
    sa.Column('contact_phone_number', sa.String(length=20), nullable=True),
    sa.Column('payment_terms', sa.String(length=100), nullable=True),
    sa.Column('bank_name', sa.String(length=100), nullable=True),
    sa.Column('iban_number', sa.String(length=34), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nif')
    )
    op.create_table('supporting_document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('document_type', sa.String(length=50), nullable=False),
    sa.Column('document_number', sa.String(length=50), nullable=False),
    sa.Column('issue_date', sa.DateTime(), nullable=False),
    sa.Column('supplier_client', sa.String(length=100), nullable=False),
    sa.Column('total_value', sa.Float(), nullable=False),
    sa.Column('observations', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tax_config',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tax_description', sa.String(length=100), nullable=False),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.Column('tax_type', sa.String(length=50), nullable=False),
    sa.Column('validity', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tax_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('units_of_measure',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('abbreviation', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('abbreviation'),
    sa.UniqueConstraint('name')
    )
    op.create_table('inventory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('movement_type', sa.String(length=20), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('reason', sa.String(length=255), nullable=True),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('target_location', sa.String(length=255), nullable=True),
    sa.Column('document_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.CheckConstraint("movement_type IN ('entry', 'exit', 'adjustment', 'transfer')", name='check_valid_movement_type'),
    sa.CheckConstraint('quantity > 0', name='check_positive_quantity'),
    sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_inventory_movement_type'), ['movement_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_inventory_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index('ix_movement_timestamp', ['movement_type', 'timestamp'], unique=False)

    op.create_table('invoices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invoice_number', sa.String(length=50), nullable=False),
    sa.Column('issue_date', sa.DateTime(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('invoice_number')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['provider_id'], ['provider.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('price_detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price_list_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('discount', sa.Float(), nullable=True),
    sa.Column('volume_price', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['price_list_id'], ['price_list.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_price_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('old_price', sa.Float(), nullable=False),
    sa.Column('new_price', sa.Float(), nullable=False),
    sa.Column('change_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('provinces',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles_permissions',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=512), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('second_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('phone_number', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('login_attempts', sa.Integer(), nullable=True),
    sa.Column('locked_until', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('audit_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('action', sa.String(length=64), nullable=False),
    sa.Column('target_type', sa.String(length=64), nullable=False),
    sa.Column('target_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('ip_address', sa.String(length=45), nullable=True),
    sa.Column('details', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('change_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('change_date', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('change_description', sa.Text(), nullable=False),
    sa.Column('affected_table', sa.String(length=50), nullable=False),
    sa.Column('affected_record_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('change_history')
    op.drop_table('audit_log')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    op.drop_table('roles_permissions')
    op.drop_table('provinces')
    op.drop_table('product_price_history')
    op.drop_table('price_detail')
    op.drop_table('order')
    op.drop_table('invoices')
    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.drop_index('ix_movement_timestamp')
        batch_op.drop_index(batch_op.f('ix_inventory_timestamp'))
        batch_op.drop_index(batch_op.f('ix_inventory_movement_type'))

    op.drop_table('inventory')
    op.drop_table('units_of_measure')
    op.drop_table('tax_types')
    op.drop_table('tax_config')
    op.drop_table('supporting_document')
    op.drop_table('suppliers')
    op.drop_table('supplier')
    op.drop_table('services')
    op.drop_table('role')
    op.drop_table('provider')
    op.drop_table('project')
    op.drop_table('products')
    op.drop_table('price_list')
    op.drop_table('permission')
    op.drop_table('inventory_item')
    op.drop_table('employee')
    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_documents_type'))
        batch_op.drop_index(batch_op.f('ix_documents_reference'))
        batch_op.drop_index('ix_document_type_date')

    op.drop_table('documents')
    op.drop_table('countries')
    op.drop_table('cost_center')
    op.drop_table('clients')
    op.drop_table('accounting_entries')
    op.drop_table('account_plan')
    # ### end Alembic commands ###
