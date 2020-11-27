"""Added active field for User

Revision ID: d002ff91c0b8
Revises: e53417f67fc8
Create Date: 2020-11-26 23:29:28.291221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd002ff91c0b8'
down_revision = 'e53417f67fc8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('active', sa.Boolean(), server_default='0', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'active')
    # ### end Alembic commands ###
