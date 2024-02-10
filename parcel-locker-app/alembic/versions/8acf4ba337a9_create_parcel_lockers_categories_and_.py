"""create parcel_lockers, categories and lockers tables

Revision ID: 8acf4ba337a9
Revises: 
Create Date: 2024-01-16 16:15:51.081392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8acf4ba337a9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'parcel_lockers',
        sa.Column('_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('address_id', sa.Integer, nullable=False, default=0)
    )

    op.create_table(
        'categories',
        sa.Column('_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('height', sa.Float, nullable=False),
        sa.Column('weight', sa.Float, nullable=False),
        sa.Column('dept', sa.Float, nullable=False)
    )

    op.create_table(
        'lockers',
        sa.Column('_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('is_empty', sa.Boolean, nullable=False, default=False),
        sa.Column('not_empty_start_date_time', sa.Integer),
        sa.Column('parcel_locker_id', sa.Integer,
                  sa.ForeignKey('parcel_lockers._id', ondelete='CASCADE', onupdate='CASCADE')),
        sa.Column('category_id', sa.Integer, sa.ForeignKey('categories._id', ondelete='CASCADE', onupdate='CASCADE'))
    )


def downgrade() -> None:
    op.drop_table("parcel_lockers")
    op.drop_table("categories")
    op.drop_table("lockers")
