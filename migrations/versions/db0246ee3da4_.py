"""empty message

Revision ID: db0246ee3da4
Revises: 
Create Date: 2019-08-07 18:49:48.330325

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'db0246ee3da4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clubs',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tournaments',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('players',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('given_name', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('club_id', postgresql.UUID(), nullable=True),
    sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['club_id'], ['clubs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('games',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('white', postgresql.UUID(), nullable=True),
    sa.Column('black', postgresql.UUID(), nullable=True),
    sa.Column('tournament_id', postgresql.UUID(), nullable=True),
    sa.Column('result', sa.Integer(), nullable=True),
    sa.Column('playing_round', sa.Integer(), nullable=True),
    sa.Column('utc_date', sa.Date(), nullable=True),
    sa.Column('utc_time', sa.Time(timezone=True), nullable=True),
    sa.Column('parsed_timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['black'], ['players.id'], ),
    sa.ForeignKeyConstraint(['tournament_id'], ['tournaments.id'], ),
    sa.ForeignKeyConstraint(['white'], ['players.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('games')
    op.drop_table('players')
    op.drop_table('tournaments')
    op.drop_table('clubs')
    # ### end Alembic commands ###