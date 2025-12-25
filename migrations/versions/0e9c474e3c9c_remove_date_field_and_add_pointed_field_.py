"""Remove date field and add pointed field to transactions

Revision ID: 0e9c474e3c9c
Revises: 
Create Date: 2025-12-25 18:17:57.831720

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e9c474e3c9c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Ajouter la colonne pointed (par défaut False)
    op.add_column('transactions', sa.Column('pointed', sa.Boolean(), nullable=False, server_default='0'))

    # Supprimer la colonne date
    with op.batch_alter_table('transactions') as batch_op:
        batch_op.drop_column('date')

    # Supprimer l'index sur period_id et date s'il existe
    try:
        op.drop_index('idx_period_date', table_name='transactions')
    except:
        pass  # L'index n'existe peut-être pas


def downgrade():
    # Réajouter la colonne date (avec une valeur par défaut temporaire)
    op.add_column('transactions', sa.Column('date', sa.Date(), nullable=False, server_default='2025-01-01'))

    # Supprimer la colonne pointed
    with op.batch_alter_table('transactions') as batch_op:
        batch_op.drop_column('pointed')

    # Recréer l'index sur period_id et date
    op.create_index('idx_period_date', 'transactions', ['period_id', 'date'])
