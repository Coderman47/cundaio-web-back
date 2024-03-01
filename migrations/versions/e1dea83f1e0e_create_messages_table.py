"""Create messages table

Revision ID: e1dea83f1e0e
Revises: 8882911292d4
Create Date: 2024-01-07 22:39:59.779084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1dea83f1e0e'
down_revision: Union[str, None] = '8882911292d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('messages',
        sa.Column('message_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('thread_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.String(length=255), nullable=False),
        sa.Column('raw_content', sa.Text(), nullable=False),
        sa.Column('content_type', sa.String(length=255), nullable=False),
        
        sa.ForeignKeyConstraint(['thread_id'], ['threads.thread_id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('message_id')
    )


def downgrade() -> None:
    op.drop_table('messages')
