"""empty message

Revision ID: 125c1197cb1a
Revises: 4bd6cd33eb93
Create Date: 2018-01-10 22:26:46.034145

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '125c1197cb1a'
down_revision = '4bd6cd33eb93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('account_number', table_name='bankdetails')
    op.drop_column('bankdetails', 'account_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bankdetails', sa.Column('account_number', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.create_index('account_number', 'bankdetails', ['account_number'], unique=True)
    # ### end Alembic commands ###
