"""empty message

Revision ID: 471e91990d7e
Revises: 31416ff324b4
Create Date: 2023-08-05 08:22:44.526849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '471e91990d7e'
down_revision = '31416ff324b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sentences', schema=None) as batch_op:
        batch_op.add_column(sa.Column('due', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sentences', schema=None) as batch_op:
        batch_op.drop_column('due')

    # ### end Alembic commands ###
