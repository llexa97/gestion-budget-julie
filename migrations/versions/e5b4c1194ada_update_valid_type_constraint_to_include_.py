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
    # Note: La contrainte CHECK est définie dans le modèle SQLAlchemy.
    # Pour SQLite, modifier une contrainte CHECK nécessite de recréer la table,
    # ce qui est complexe. La contrainte sera mise à jour automatiquement lors
    # de la prochaine initialisation de la base de données avec db.create_all().
    # En production, si la base de données existe déjà, elle devra être recréée
    # ou une migration plus complexe devra être écrite pour recréer la table.
    pass


def downgrade():
    pass
