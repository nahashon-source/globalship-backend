"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2025-01-15

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('email', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('company_name', sa.String(255), nullable=True),
        sa.Column('phone', sa.String(50), nullable=True),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_verified', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('last_login', sa.DateTime(), nullable=True),
    )
    
    # Create shipments table
    op.create_table(
        'shipments',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('tracking_number', sa.String(50), nullable=False, unique=True, index=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('origin_city', sa.String(100), nullable=False),
        sa.Column('origin_country', sa.String(100), nullable=False),
        sa.Column('origin_address', sa.String(500), nullable=True),
        sa.Column('origin_postal_code', sa.String(20), nullable=True),
        sa.Column('destination_city', sa.String(100), nullable=False),
        sa.Column('destination_country', sa.String(100), nullable=False),
        sa.Column('destination_address', sa.String(500), nullable=True),
        sa.Column('destination_postal_code', sa.String(20), nullable=True),
        sa.Column('service_type', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, index=True),
        sa.Column('weight', sa.Numeric(10, 2), nullable=True),
        sa.Column('dimensions', sa.JSON(), nullable=True),
        sa.Column('package_count', sa.Numeric(10, 0), nullable=False, default=1),
        sa.Column('estimated_cost', sa.Numeric(10, 2), nullable=True),
        sa.Column('actual_cost', sa.Numeric(10, 2), nullable=True),
        sa.Column('currency', sa.String(3), nullable=False, default='USD'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('estimated_delivery', sa.DateTime(), nullable=True),
        sa.Column('actual_delivery', sa.DateTime(), nullable=True),
        sa.Column('special_instructions', sa.String(1000), nullable=True),
        sa.Column('insurance', sa.Boolean(), nullable=False, default=False),
        sa.Column('signature_required', sa.Boolean(), nullable=False, default=False),
    )
    
    # Create shipment_events table
    op.create_table(
        'shipment_events',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('shipment_id', UUID(as_uuid=True), sa.ForeignKey('shipments.id'), nullable=False, index=True),
        sa.Column('event_type', sa.String(100), nullable=False),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
    )
    
    # Create quotes table
    op.create_table(
        'quotes',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('origin', sa.String(255), nullable=False),
        sa.Column('destination', sa.String(255), nullable=False),
        sa.Column('service_type', sa.String(50), nullable=False),
        sa.Column('weight', sa.Numeric(10, 2), nullable=True),
        sa.Column('dimensions', sa.String(255), nullable=True),
        sa.Column('package_count', sa.Numeric(10, 0), nullable=False, default=1),
        sa.Column('estimated_cost', sa.Numeric(10, 2), nullable=True),
        sa.Column('currency', sa.String(3), nullable=False, default='USD'),
        sa.Column('status', sa.String(50), nullable=False, index=True),
        sa.Column('special_requirements', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
    )
    
    # Create contact_messages table
    op.create_table(
        'contact_messages',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False, index=True),
        sa.Column('phone', sa.String(50), nullable=True),
        sa.Column('subject', sa.String(500), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, index=True),
        sa.Column('admin_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()'), index=True),
        sa.Column('read_at', sa.DateTime(), nullable=True),
        sa.Column('responded_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('contact_messages')
    op.drop_table('quotes')
    op.drop_table('shipment_events')
    op.drop_table('shipments')
    op.drop_table('users')
