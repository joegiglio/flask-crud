"""Added fields for User

Revision ID: e53417f67fc8
Revises: 78b6bb4e24d1
Create Date: 2020-11-26 23:09:20.652593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e53417f67fc8'
down_revision = '78b6bb4e24d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('confirmed_at', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('last_active', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('verification_token', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'verification_token')
    op.drop_column('user', 'last_active')
    op.drop_column('user', 'confirmed_at')
    # ### end Alembic commands ###
