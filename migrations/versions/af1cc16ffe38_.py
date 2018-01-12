"""empty message

Revision ID: af1cc16ffe38
Revises: 972d83ac636e
Create Date: 2018-01-12 23:33:09.105053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af1cc16ffe38'
down_revision = '972d83ac636e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('road', sa.String(length=400), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'road')
    # ### end Alembic commands ###
