"""Initial migration

Revision ID: 3ee09780d0b7
Revises: 
Create Date: 2024-10-14 12:39:33.747948

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ee09780d0b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('agenda', sa.Column('speaker_id', sa.Integer()))
    op.create_foreign_key(None, 'agenda', 'speakers', ['speaker_id'], ['id'])
    op.add_column('apply_form', sa.Column('email', sa.String(length=50)))
    op.add_column('apply_form', sa.Column('employment_states', sa.String(length=255)))
    op.drop_column('apply_form', 'years_of_experience')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apply_form', sa.Column('years_of_experience', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
    op.drop_column('apply_form', 'employment_states')
    op.drop_column('apply_form', 'email')
    op.drop_constraint(None, 'agenda', type_='foreignkey')
    op.drop_column('agenda', 'speaker_id')
    # ### end Alembic commands ###
