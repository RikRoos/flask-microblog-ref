"""messages

Revision ID: 2878c21376a8
Revises: 71ce880c1dce
Create Date: 2025-07-16 21:27:24.872547

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2878c21376a8'
down_revision = '71ce880c1dce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mb_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('recipient_id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['recipient_id'], ['mb_users.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['mb_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('mb_messages', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_mb_messages_recipient_id'), ['recipient_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_mb_messages_sender_id'), ['sender_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_mb_messages_timestamp'), ['timestamp'], unique=False)

    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_message_recipient_id'))
        batch_op.drop_index(batch_op.f('ix_message_sender_id'))
        batch_op.drop_index(batch_op.f('ix_message_timestamp'))

    op.drop_table('message')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('sender_id', sa.INTEGER(), nullable=False),
    sa.Column('recipient_id', sa.INTEGER(), nullable=False),
    sa.Column('body', sa.VARCHAR(length=140), nullable=False),
    sa.Column('timestamp', sa.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['recipient_id'], ['mb_users.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['mb_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_message_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_message_sender_id'), ['sender_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_message_recipient_id'), ['recipient_id'], unique=False)

    with op.batch_alter_table('mb_messages', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_mb_messages_timestamp'))
        batch_op.drop_index(batch_op.f('ix_mb_messages_sender_id'))
        batch_op.drop_index(batch_op.f('ix_mb_messages_recipient_id'))

    op.drop_table('mb_messages')
    # ### end Alembic commands ###
