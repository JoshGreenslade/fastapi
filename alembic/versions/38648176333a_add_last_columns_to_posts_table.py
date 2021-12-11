"""Add last columns to posts table

Revision ID: 38648176333a
Revises: c55435d5283a
Create Date: 2021-12-11 09:53:32.493273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "38648176333a"
down_revision = "c55435d5283a"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )


def downgrade():
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
