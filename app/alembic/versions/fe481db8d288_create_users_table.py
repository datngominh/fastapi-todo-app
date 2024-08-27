"""create_users_table

Revision ID: fe481db8d288
Revises: 62d9d645086d
Create Date: 2024-08-27 16:03:42.968454

"""
from alembic import op
import sqlalchemy as sa

from uuid import uuid4
from datetime import datetime, timezone
from schemas.user import get_password_hash
from settings import ADMIN_DEFAULT_PASSWORD

# revision identifiers, used by Alembic.
revision = 'fe481db8d288'
down_revision = '62d9d645086d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    user_table = op.create_table(
        'users',
        sa.Column("id", sa.UUID, nullable=False, primary_key=True),
        sa.Column('email', sa.String(), unique=True, index=True, nullable=False),
        sa.Column('username', sa.String(), unique=True, index=True, nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_admin', sa.Boolean(), default=False),
        sa.Column('company_id', sa.UUID, nullable=True),
    )
    
    op.create_index("idx_usr_fst_lst_name", "users", ["first_name", "last_name"])
    
    op.create_foreign_key("fk_user_company", "users", "companies", ["company_id"],['id'])

    # Data seed for first user
    op.bulk_insert(user_table, [
        {
            "id": uuid4(),
            "email": "fastapi_tour@sample.com", 
            "username": "fa_admin",
            "password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
            "first_name": "FastApi",
            "last_name": "Admin",
            "is_active": True,
            "is_admin": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
    ])


def downgrade() -> None:
    op.drop_constraint("fk_user_company", "users", type_="foreignkey")
    op.drop_index("idx_usr_fst_lst_name", "users")
    op.drop_table('users')
