"""AccountOrm: убран с deleted_at nullable False

Revision ID: 3886cb352091
Revises: beef7e547d41
Create Date: 2025-10-02 17:04:49.576605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3886cb352091'
down_revision: Union[str, Sequence[str], None] = 'beef7e547d41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    def upgrade() -> None:
        pass

    def downgrade() -> None:
        pass
