"""add_job_and_status_fields

Revision ID: 661c42e686b5
Revises: 001
Create Date: 2026-02-09 19:50:24.620842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '661c42e686b5'
down_revision: Union[str, Sequence[str], None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('videos', sa.Column('telegram_user_id', sa.Integer(), nullable=True))
    op.add_column('videos', sa.Column('processing_status', sa.String(), nullable=False, server_default='pending'))
    op.add_column('videos', sa.Column('job_id', sa.String(), nullable=True))
    op.add_column('videos', sa.Column('error_message', sa.Text(), nullable=True))
    op.add_column('videos', sa.Column('processed_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('videos', 'processed_at')
    op.drop_column('videos', 'error_message')
    op.drop_column('videos', 'job_id')
    op.drop_column('videos', 'processing_status')
    op.drop_column('videos', 'telegram_user_id')
