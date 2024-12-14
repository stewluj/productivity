"""Add partner_id to User model

Revision ID: 31d169e1f9c6
Revises: 
Create Date: 2024-12-03 22:42:03.199674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31d169e1f9c6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('note')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('partner_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['partner_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('partner_id')

    op.create_table('note',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('data', sa.VARCHAR(length=10000), nullable=True),
    sa.Column('date', sa.DATETIME(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
