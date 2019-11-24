"""empty message

Revision ID: 7013c1ae63f7
Revises: 98d44822d3cf
Create Date: 2019-11-24 00:59:22.115481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7013c1ae63f7'
down_revision = '98d44822d3cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alarm',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hour', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sensor_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('temperature', sa.Integer(), nullable=False),
    sa.Column('humidity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('song',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('song', sa.String(length=2500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('message')
    op.drop_index('ix_user_email', table_name='user')
    op.drop_index('ix_user_username', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_username', 'user', ['username'], unique=1)
    op.create_index('ix_user_email', 'user', ['email'], unique=1)
    op.create_table('message',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('direction', sa.VARCHAR(length=64), nullable=True),
    sa.Column('message', sa.VARCHAR(length=2500), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('time', sa.VARCHAR(length=6), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('song')
    op.drop_table('sensor_data')
    op.drop_table('alarm')
    # ### end Alembic commands ###