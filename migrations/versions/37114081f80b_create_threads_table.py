"""Create threads table

Revision ID: 37114081f80b
Revises: a144149f3ba7
Create Date: 2024-01-07 22:36:40.465762

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37114081f80b'
down_revision: Union[str, None] = 'a144149f3ba7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('threads',
        sa.Column('thread_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('instructions', sa.Text(), nullable=True),
        sa.Column('openai_assistant_id', sa.String(length=255), nullable=True),
        sa.Column('openai_thread_id', sa.String(length=255), nullable=True),
        
        sa.PrimaryKeyConstraint('thread_id')
    )


def downgrade() -> None:
    op.drop_table('threads')
