"""Allow zero amount in transactions

Revision ID: 4e61169cc91a
Revises: e5b4c1194ada
Create Date: 2025-12-25 18:59:18.763856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e61169cc91a'
down_revision = 'e5b4c1194ada'
branch_labels = None
depends_on = None


def upgrade():
    # Pour SQLite : modifier une contrainte CHECK nécessite de recréer la table
    # batch_alter_table gère automatiquement la recréation de la table
    with op.batch_alter_table('transactions', schema=None, copy_from=None,
                               table_kwargs={
                                   'sqlite_autoincrement': True
                               }) as batch_op:
        # Supprimer l'ancienne contrainte et en ajouter une nouvelle
        batch_op.drop_constraint('positive_amount', type_='check')
        batch_op.create_check_constraint('positive_amount', 'amount >= 0')


def downgrade():
    # Retour à la contrainte stricte (amount > 0)
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.drop_constraint('positive_amount', type_='check')
        batch_op.create_check_constraint('positive_amount', 'amount > 0')
