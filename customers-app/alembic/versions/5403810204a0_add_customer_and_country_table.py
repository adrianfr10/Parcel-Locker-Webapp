"""add customer and country table

Revision ID: 5403810204a0
Revises: 
Create Date: 2023-12-04 18:20:23.127369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5403810204a0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'countries',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=30), unique=True, nullable=False),
    )

    op.create_table(
        'customers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=30), nullable=False),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('country_id', sa.Integer(), sa.ForeignKey('countries.id'))
    )


def downgrade() -> None:
    op.drop_table('countries')
    op.drop_table('customers')
