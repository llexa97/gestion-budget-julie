"""remove_date_column_from_transactions

Revision ID: ea94c8464207
Revises: ec51fe643eaa
Create Date: 2025-12-25 21:37:26.231558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea94c8464207'
down_revision = 'ec51fe643eaa'
branch_labels = None
depends_on = None


def upgrade():
    # SQLite ne supporte pas DROP COLUMN directement avec batch_alter_table
    # On doit utiliser copy_from pour spécifier les colonnes à garder
    with op.batch_alter_table('transactions', schema=None, copy_from=sa.Table(
        'transactions',
        sa.MetaData(),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('period_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=10), nullable=False),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('label', sa.String(length=200), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('pointed', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['period_id'], ['periods.id']),
        sa.CheckConstraint('amount >= 0', name='positive_amount'),
        sa.CheckConstraint("type IN ('ENTREE', 'DEPENSE', 'EPARGNE')", name='valid_type'),
    )) as batch_op:
        # La colonne 'date' sera automatiquement supprimée car elle n'est pas dans copy_from
        pass

    # Recréer l'index
    op.create_index('idx_period_type', 'transactions', ['period_id', 'type'], unique=False)


def downgrade():
    # Rajouter la colonne date si on fait un rollback
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.Date(), nullable=True))
