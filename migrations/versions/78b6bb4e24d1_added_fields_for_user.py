"""Added fields for User

Revision ID: 78b6bb4e24d1
Revises: ad4c9eb6cecb
Create Date: 2020-11-24 20:58:09.764716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78b6bb4e24d1'
down_revision = 'ad4c9eb6cecb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('login_count', sa.Integer(), server_default='0', nullable=True))
    op.add_column('user', sa.Column('password', sa.String(length=255), server_default='', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'password')
    op.drop_column('user', 'login_count')
    # ### end Alembic commands ###
