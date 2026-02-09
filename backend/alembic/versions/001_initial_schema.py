"""initial_schema

Revision ID: 001
Revises:
Create Date: 2026-02-09 18:35:17.270267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import pgvector
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')

    op.create_table(
        'videos',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('thumbnail', sa.String(), nullable=True),
        sa.Column('transcript', sa.Text(), nullable=True),
        sa.Column('tags', postgresql.ARRAY(sa.String()), server_default='{}', nullable=True),
        sa.Column('category', sa.Enum('recetas', 'fitness', 'viajes', 'educacion', 'entretenimiento', 'otros', name='category'), nullable=True),
        sa.Column('ingredients', postgresql.ARRAY(sa.String()), server_default='{}', nullable=True),
        sa.Column('steps', postgresql.ARRAY(sa.String()), server_default='{}', nullable=True),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('source', sa.Enum('instagram', 'tiktok', name='videosource'), nullable=False),
        sa.Column('saved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('user_note', sa.Text(), nullable=True),
        sa.Column('embedding', Vector(384), nullable=True),
        sa.Column('language', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('videos')
    op.execute('DROP TYPE category')
    op.execute('DROP TYPE videosource')
