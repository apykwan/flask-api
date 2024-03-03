"""Added Foreign Key

Revision ID: 5e64d1c37bd3
Revises: 6e44f8e0447c
Create Date: 2024-02-28 16:58:27.359175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e64d1c37bd3'
down_revision = '6e44f8e0447c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('poster_id', sa.String(length=200), nullable=True))
        batch_op.create_foreign_key(None, 'users', ['poster_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('poster_id')

    # ### end Alembic commands ###