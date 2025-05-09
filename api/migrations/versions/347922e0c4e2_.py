"""empty message

Revision ID: 347922e0c4e2
Revises: 471e91990d7e
Create Date: 2023-08-05 08:55:50.434339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '347922e0c4e2'
down_revision = '471e91990d7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_words')
    with op.batch_alter_table('words', schema=None) as batch_op:
        batch_op.alter_column('seen',
               existing_type=sa.BOOLEAN(),
               nullable=False)
        batch_op.alter_column('interval',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('easing_factor',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('words', schema=None) as batch_op:
        batch_op.alter_column('easing_factor',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('interval',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('seen',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    op.create_table('_alembic_tmp_words',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('text', sa.VARCHAR(length=500), nullable=False),
    sa.Column('gloss', sa.VARCHAR(length=500), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('sentence_id', sa.INTEGER(), nullable=True),
    sa.Column('last_review', sa.DATETIME(), nullable=True),
    sa.Column('pos', sa.INTEGER(), nullable=False),
    sa.Column('seen', sa.BOOLEAN(), nullable=False),
    sa.Column('due', sa.DATETIME(), nullable=True),
    sa.Column('interval', sa.INTEGER(), nullable=False),
    sa.Column('easing_factor', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['sentence_id'], ['sentences.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
