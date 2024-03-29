"""empty message

Revision ID: ac9aa863c989
Revises: bb88962c719e
Create Date: 2019-08-08 20:29:51.463263

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac9aa863c989'
down_revision = 'bb88962c719e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('raw', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'games', ['raw'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'games', type_='unique')
    op.drop_column('games', 'raw')
    # ### end Alembic commands ###
