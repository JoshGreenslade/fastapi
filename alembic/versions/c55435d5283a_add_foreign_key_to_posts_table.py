"""add foreign-key to posts table

Revision ID: c55435d5283a
Revises: 0a8249cb88c1
Create Date: 2021-12-11 09:50:34.712952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c55435d5283a"
down_revision = "0a8249cb88c1"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade():
    op.drop_constraint("posts_users_fk", table_name='posts')
    op.drop_column('posts', 'owner_id')
