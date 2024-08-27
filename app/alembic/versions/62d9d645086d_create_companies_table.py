"""create_companies_table

Revision ID: 62d9d645086d
Revises: 
Create Date: 2024-08-27 13:57:34.024282

"""
from alembic import op
import sqlalchemy as sa

from schemas.company import Company_Mode, Company_Rating


# revision identifiers, used by Alembic.
revision = '62d9d645086d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'companies',
        sa.Column("id", sa.UUID, nullable=False, primary_key=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('name', sa.String(1000), nullable=False),
        sa.Column('description', sa.String(2000), nullable=False),
        sa.Column('mode', sa.Enum(Company_Mode), nullable=False, default=Company_Mode.Active),
        sa.Column('rating', sa.Enum(Company_Rating), nullable=False, default=Company_Rating.MEDIUM),
    )


def downgrade() -> None:
    op.drop_table('companies')
