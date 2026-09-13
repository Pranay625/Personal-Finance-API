"""initial migration

Revision ID: 000ca241b62a
Revises:
Create Date: 2026-09-12 23:10:45.225488
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "000ca241b62a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Mark the existing database as the initial schema."""
    pass


def downgrade() -> None:
    """No schema changes to reverse."""
    pass