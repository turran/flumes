"""empty message

Revision ID: 30374e2904cd
Revises: ad35ceceeb92
Create Date: 2022-02-03 09:22:27.872511

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "30374e2904cd"
down_revision = "ad35ceceeb92"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('infos') as batch_op:
            batch_op.alter_column('duration', type_=sa.BigInteger(), existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('infos') as batch_op:
            batch_op.alter_column('duration', type_=sa.INTEGER(), existing_nullable=True)
    # ### end Alembic commands ###