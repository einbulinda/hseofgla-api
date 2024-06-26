"""initial commit

Revision ID: d571baff3a30
Revises: 
Create Date: 2024-04-18 16:38:38.931730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd571baff3a30'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('staff',
    sa.Column('staff_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('mobile_number', sa.String(length=15), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('role', sa.String(length=255), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.Column('updated_date', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['dev.staff.staff_id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['dev.staff.staff_id'], ),
    sa.PrimaryKeyConstraint('staff_id'),
    schema='dev'
    )
    op.create_table('customers',
    sa.Column('customer_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('mobile_number', sa.String(length=15), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('credit_balance', sa.Numeric(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.Column('updated_date', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['dev.staff.staff_id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['dev.staff.staff_id'], ),
    sa.PrimaryKeyConstraint('customer_id'),
    schema='dev'
    )
    op.create_table('login_details',
    sa.Column('loggin_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('staff_id', sa.Integer(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.Column('updated_date', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['dev.staff.staff_id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['dev.customers.customer_id'], ),
    sa.ForeignKeyConstraint(['staff_id'], ['dev.staff.staff_id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['dev.staff.staff_id'], ),
    sa.PrimaryKeyConstraint('loggin_id'),
    sa.UniqueConstraint('username'),
    schema='aud'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('login_details', schema='aud')
    op.drop_table('customers', schema='dev')
    op.drop_table('staff', schema='dev')
    # ### end Alembic commands ###
