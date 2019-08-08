"""empty message

Revision ID: d789da95aa1b
Revises: 940b135043c9
Create Date: 2019-08-08 22:27:46.690043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd789da95aa1b'
down_revision = '940b135043c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_ply', 'plies', ['current_position', 'next_position', 'game_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_ply', 'plies', type_='unique')
    # ### end Alembic commands ###