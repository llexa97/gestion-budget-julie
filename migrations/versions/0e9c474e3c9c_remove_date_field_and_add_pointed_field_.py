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
    # Cette migration est désactivée car l'application utilise db.create_all()
    # qui crée directement les tables avec la structure finale.
    # Si vous avez une base de données existante avec l'ancienne structure,
    # utilisez les scripts de migration manuels.
    pass


def downgrade():
    # Downgrade désactivé - voir upgrade()
    pass
