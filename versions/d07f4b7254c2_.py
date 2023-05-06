"""empty message

Revision ID: d07f4b7254c2
Revises: 1798d1f0c823
Create Date: 2023-05-06 06:30:27.376619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd07f4b7254c2'
down_revision = '1798d1f0c823'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('twitter_link', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('instagram_link', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.drop_column('instagram_link')
        batch_op.drop_column('twitter_link')

    # ### end Alembic commands ###
