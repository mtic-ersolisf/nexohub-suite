"""add tenants and parking_lots, add tenant_id to users

Revision ID: 3c7093111183
Revises: befa4a157feb
Create Date: 2025-12-26 16:06:47.977506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c7093111183'
down_revision: Union[str, Sequence[str], None] = 'befa4a157feb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
