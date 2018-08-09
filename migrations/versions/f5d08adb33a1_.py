"""empty message

Revision ID: f5d08adb33a1
Revises: 32fad2464781
Create Date: 2018-08-09 13:35:16.080263

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f5d08adb33a1'
down_revision = '32fad2464781'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.Column('urole', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.drop_table('ar_internal_metadata')
    op.drop_table('schema_migrations')
    op.drop_table('User')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('items',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('done', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('todo_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['todo_id'], ['todos.id'], name='fk_rails_c01e6b449d'),
    sa.PrimaryKeyConstraint('id', name='items_pkey')
    )
    op.create_index('index_items_on_todo_id', 'items', ['todo_id'], unique=False)
    op.create_table('todos',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_by', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='todos_pkey')
    )
    op.create_table('User',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"User_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('pwd_hash', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('urole', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='User_pkey'),
    sa.UniqueConstraint('email', name='User_email_key'),
    sa.UniqueConstraint('username', name='User_username_key')
    )
    op.create_table('schema_migrations',
    sa.Column('version', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('version', name='schema_migrations_pkey')
    )
    op.create_table('ar_internal_metadata',
    sa.Column('key', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('value', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('key', name='ar_internal_metadata_pkey')
    )
    op.drop_table('users')
    # ### end Alembic commands ###
