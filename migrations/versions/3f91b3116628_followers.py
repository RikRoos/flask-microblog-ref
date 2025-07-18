"""followers

Revision ID: 3f91b3116628
Revises: 77386ce04e71
Create Date: 2025-06-24 19:18:58.258798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f91b3116628'
down_revision = '77386ce04e71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mb_followers',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['followed_id'], ['mb_users.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['mb_users.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mb_followers')
    # ### end Alembic commands ###
