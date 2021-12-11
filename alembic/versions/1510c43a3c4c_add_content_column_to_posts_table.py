"""add content column to posts table

Revision ID: 1510c43a3c4c
Revises: afaeadbb2745
Create Date: 2021-12-11 09:42:33.155478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1510c43a3c4c"
down_revision = "afaeadbb2745"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade():
    op.drop_column("posts", "content")
