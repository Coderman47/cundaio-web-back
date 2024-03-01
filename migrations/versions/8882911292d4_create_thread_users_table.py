"""Create thread_users table

Revision ID: 8882911292d4
Revises: 37114081f80b
Create Date: 2024-01-07 22:38:37.156805

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8882911292d4'
down_revision: Union[str, None] = '37114081f80b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('thread_users',
        sa.Column('thread_user_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('thread_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        
        sa.ForeignKeyConstraint(['thread_id'], ['threads.thread_id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('thread_user_id'),
        sa.UniqueConstraint('thread_id', 'user_id', name='thread_user_unique')
    )


def downgrade() -> None:
    op.drop_table('thread_users')
