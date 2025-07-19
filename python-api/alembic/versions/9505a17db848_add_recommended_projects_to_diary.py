"""add recommended_projects to diary

Revision ID: 9505a17db848
Revises: 1dc0b2525455
Create Date: 2025-07-18 01:04:46.532071

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9505a17db848'
down_revision = '1dc0b2525455'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('diary', sa.Column('recommended_projects', sa.Text(), nullable=True))

def downgrade() -> None:
    op.drop_column('diary', 'recommended_projects')
