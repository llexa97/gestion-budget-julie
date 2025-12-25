#!/usr/bin/env python3
"""
Script pour supprimer la colonne 'date' de la table transactions
"""
from app import create_app, db

def remove_date_column():
    app = create_app()

    with app.app_context():
        print("🔍 Suppression de la colonne 'date' de la table transactions...")

        try:
            # SQLite ne supporte pas DROP COLUMN directement
            # On doit recréer la table sans la colonne date
            with db.engine.begin() as connection:
                # Créer une table temporaire sans la colonne date
                connection.execute(db.text("""
                    CREATE TABLE transactions_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        period_id INTEGER NOT NULL,
                        type VARCHAR(10) NOT NULL,
                        amount NUMERIC(10, 2) NOT NULL,
                        label VARCHAR(200) NOT NULL,
                        category VARCHAR(100),
                        notes TEXT,
                        pointed BOOLEAN NOT NULL DEFAULT 0,
                        created_at DATETIME,
                        updated_at DATETIME,
                        FOREIGN KEY (period_id) REFERENCES periods(id),
                        CHECK (amount >= 0),
                        CHECK (type IN ('ENTREE', 'DEPENSE', 'EPARGNE'))
                    )
                """))

                # Copier les données (sans la colonne date)
                connection.execute(db.text("""
                    INSERT INTO transactions_new
                    (id, period_id, type, amount, label, category, notes, pointed, created_at, updated_at)
                    SELECT id, period_id, type, amount, label, category, notes, pointed, created_at, updated_at
                    FROM transactions
                """))

                # Supprimer l'ancienne table
                connection.execute(db.text("DROP TABLE transactions"))

                # Renommer la nouvelle table
                connection.execute(db.text("ALTER TABLE transactions_new RENAME TO transactions"))

                # Recréer l'index
                connection.execute(db.text("""
                    CREATE INDEX idx_period_type ON transactions (period_id, type)
                """))

            print("✅ Colonne 'date' supprimée avec succès!")
            print("✅ Toutes les données ont été préservées!")
            return True

        except Exception as e:
            print(f"❌ Erreur lors de la suppression: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    print("=" * 60)
    print("  Script de suppression de la colonne 'date'")
    print("=" * 60)
    print()

    success = remove_date_column()

    print()
    if success:
        print("✅ Opération terminée avec succès!")
        print("👉 Redémarrez maintenant le service avec:")
        print("   sudo systemctl restart budget-manager")
    else:
        print("❌ Échec de l'opération")
    print()
