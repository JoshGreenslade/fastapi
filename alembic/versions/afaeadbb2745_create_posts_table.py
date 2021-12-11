"""create posts table

Revision ID: afaeadbb2745
Revises: 
Create Date: 2021-12-11 09:37:31.190353

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = "afaeadbb2745"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table("posts")
