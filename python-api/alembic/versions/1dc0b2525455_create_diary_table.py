"""create diary table

Revision ID: 1dc0b2525455
Revises: 
Create Date: 2025-07-18 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision = '1dc0b2525455'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'diary',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('sentiment', sa.String(length=16), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_diary_id', 'diary', ['id'], unique=False)

def downgrade():
    op.drop_index('ix_diary_id', table_name='diary')
    op.drop_table('diary')
