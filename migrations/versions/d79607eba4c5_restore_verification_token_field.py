"""Restore verification token field.

Revision ID: d79607eba4c5
Revises: 3bfa9c4ea4e8
Create Date: 2020-11-29 22:28:22.337621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd79607eba4c5'
down_revision = '3bfa9c4ea4e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('verification_token', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'verification_token')
    # ### end Alembic commands ###
