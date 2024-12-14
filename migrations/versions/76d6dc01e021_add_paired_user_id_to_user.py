"""Add paired_user_id to User

Revision ID: 76d6dc01e021
Revises: 
Create Date: 2024-12-04 00:07:17.207033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76d6dc01e021'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('paired_user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['paired_user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('paired_user_id')

    # ### end Alembic commands ###
