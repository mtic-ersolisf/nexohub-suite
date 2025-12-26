"""init

Revision ID: 85a3499babe2
Revises: 717166252644
Create Date: 2025-12-19 14:07:26.685667

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85a3499babe2'
down_revision: Union[str, Sequence[str], None] = '717166252644'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
