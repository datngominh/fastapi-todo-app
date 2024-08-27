"""create_tasks_table

Revision ID: 4532adb75ee1
Revises: fe481db8d288
Create Date: 2024-08-27 16:24:13.774980

"""
from alembic import op
import sqlalchemy as sa

from schemas.task import Task_Priority, Task_Status


# revision identifiers, used by Alembic.
revision = '4532adb75ee1'
down_revision = 'fe481db8d288'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column("id", sa.UUID, nullable=False, primary_key=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('sumary', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('status', sa.Enum(Task_Status), nullable=False, default=Task_Status.TODO),
        sa.Column('priority', sa.Enum(Task_Priority), nullable=False, default=Task_Priority.MEDIUM),
        sa.Column('user_id', sa.UUID, nullable=True),
    )
    
    op.create_index("idx_usr_uid_sum", "tasks", ["user_id", "sumary"])
    
    op.create_foreign_key("fk_task_user", "tasks", "users", ["user_id"],['id'])


def downgrade() -> None:
    op.drop_index("idx_usr_uid_sum", "tasks")
    op.drop_constraint("fk_task_user", "tasks", type_="foreignkey")
    op.drop_table("tasks")
    pass
