"""Create questions table

Revision ID: d75b229a3056
Revises: e1dea83f1e0e
Create Date: 2024-01-08 12:01:32.480479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd75b229a3056'
down_revision: Union[str, None] = 'e1dea83f1e0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('questions',
        sa.Column('question_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.String(length=255), nullable=False),
        sa.Column('answer', sa.Text(), nullable=True),
        sa.Column('message_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        
        sa.ForeignKeyConstraint(['message_id'], ['messages.message_id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('question_id')
    )


def downgrade() -> None:
    op.drop_table('questions')
