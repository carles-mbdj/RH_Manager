"""Initialisation propre

Revision ID: fb548a85af3c
Revises: 
Create Date: 2025-07-05 12:42:52.448388

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fb548a85af3c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('absence', schema=None) as batch_op:
        batch_op.add_column(sa.Column('etat', sa.String(length=50), nullable=True))
        batch_op.alter_column('employe_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
        batch_op.drop_column('statut')

    with op.batch_alter_table('demande_conge', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reference', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('employe_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('type', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('duree', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('approbateur_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('date_creation', sa.DateTime(), nullable=True))
        batch_op.alter_column('date_debut',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.alter_column('date_fin',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.alter_column('statut',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=20),
               existing_nullable=True)
        batch_op.create_unique_constraint(None, ['reference'])
        batch_op.drop_constraint(batch_op.f('demande_conge_ibfk_1'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'employee', ['employe_id'], ['id'])
        batch_op.create_foreign_key(None, 'utilisateur', ['approbateur_id'], ['id'])
        batch_op.drop_column('nom')
        batch_op.drop_column('date_soumission')
        batch_op.drop_column('type_conge_id')
        batch_op.drop_column('telephone')

    with op.batch_alter_table('offre_emploi', schema=None) as batch_op:
        batch_op.drop_column('publie')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('offre_emploi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('publie', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))

    with op.batch_alter_table('demande_conge', schema=None) as batch_op:
        batch_op.add_column(sa.Column('telephone', mysql.VARCHAR(length=20), nullable=False))
        batch_op.add_column(sa.Column('type_conge_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('date_soumission', mysql.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('nom', mysql.VARCHAR(length=100), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('demande_conge_ibfk_1'), 'type_conge', ['type_conge_id'], ['id'])
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('statut',
               existing_type=sa.String(length=20),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=True)
        batch_op.alter_column('date_fin',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.alter_column('date_debut',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.drop_column('date_creation')
        batch_op.drop_column('approbateur_id')
        batch_op.drop_column('duree')
        batch_op.drop_column('type')
        batch_op.drop_column('employe_id')
        batch_op.drop_column('reference')

    with op.batch_alter_table('absence', schema=None) as batch_op:
        batch_op.add_column(sa.Column('statut', mysql.VARCHAR(length=50), nullable=True))
        batch_op.alter_column('employe_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
        batch_op.drop_column('etat')

    # ### end Alembic commands ###
