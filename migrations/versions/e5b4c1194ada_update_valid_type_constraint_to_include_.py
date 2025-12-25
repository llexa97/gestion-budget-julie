"""Update valid_type constraint to include EPARGNE

Revision ID: e5b4c1194ada
Revises: 0e9c474e3c9c
Create Date: 2025-12-25 18:42:12.021251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5b4c1194ada'
down_revision = '0e9c474e3c9c'
branch_labels = None
depends_on = None


def upgrade():
    # Pour SQLite : modifier une contrainte CHECK nécessite de recréer la table
    # batch_alter_table gère automatiquement la recréation de la table
    with op.batch_alter_table('transactions', schema=None, copy_from=None,
                               table_kwargs={
                                   'sqlite_autoincrement': True
                               }) as batch_op:
        # Supprimer l'ancienne contrainte et en ajouter une nouvelle avec EPARGNE
        batch_op.drop_constraint('valid_type', type_='check')
        batch_op.create_check_constraint('valid_type', "type IN ('ENTREE', 'DEPENSE', 'EPARGNE')")


def downgrade():
    # Retour à la contrainte sans EPARGNE
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.drop_constraint('valid_type', type_='check')
        batch_op.create_check_constraint('valid_type', "type IN ('ENTREE', 'DEPENSE')")
