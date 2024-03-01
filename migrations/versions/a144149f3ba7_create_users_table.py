"""Create users table

Revision ID: a144149f3ba7
Revises: 
Create Date: 2024-01-07 21:01:03.806000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a144149f3ba7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('given_name', sa.String(length=255), nullable=False),
        sa.Column('last_name', sa.String(length=255), nullable=False),
        sa.Column('corpoweb', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('token', sa.Text(), nullable=True),
        
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email', name='user_email_unique')
    )


def downgrade() -> None:
    op.drop_table('users')
