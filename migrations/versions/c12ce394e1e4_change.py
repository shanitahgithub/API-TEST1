"""change

Revision ID: c12ce394e1e4
Revises: efc8d50c0382
Create Date: 2024-04-02 21:29:05.975823

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c12ce394e1e4'
down_revision = 'efc8d50c0382'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=mysql.TINYTEXT(),
               type_=sa.Text(length=255),
               existing_nullable=False)
        batch_op.alter_column('user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('biography',
               existing_type=mysql.TINYTEXT(),
               type_=sa.Text(length=255),
               existing_nullable=True)
        batch_op.alter_column('password',
               existing_type=mysql.TINYTEXT(),
               type_=sa.Text(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.Text(length=255),
               type_=mysql.TINYTEXT(),
               existing_nullable=False)
        batch_op.alter_column('biography',
               existing_type=sa.Text(length=255),
               type_=mysql.TINYTEXT(),
               existing_nullable=True)

    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
        batch_op.alter_column('description',
               existing_type=sa.Text(length=255),
               type_=mysql.TINYTEXT(),
               existing_nullable=False)

    # ### end Alembic commands ###
