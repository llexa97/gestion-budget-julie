"""add_pointed_field_to_transactions

Revision ID: ec51fe643eaa
Revises: 4e61169cc91a
Create Date: 2025-12-25 19:36:21.302850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec51fe643eaa'
down_revision = '4e61169cc91a'
branch_labels = None
depends_on = None


def upgrade():
    # Ajouter la colonne 'pointed' avec une valeur par défaut False
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pointed', sa.Boolean(), nullable=True, server_default='0'))

    # Mettre à jour les valeurs NULL en False (par sécurité)
    op.execute("UPDATE transactions SET pointed = 0 WHERE pointed IS NULL")

    # Rendre la colonne NOT NULL après avoir mis à jour les valeurs
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.alter_column('pointed', nullable=False)


def downgrade():
    # Supprimer la colonne 'pointed'
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.drop_column('pointed')
