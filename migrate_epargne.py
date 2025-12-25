"""
Script de migration pour ajouter le support d'EPARGNE dans la base de données.
Ce script met à jour la contrainte CHECK de la table transactions pour accepter 'EPARGNE'.
"""
import sqlite3
import os

def migrate_database():
    """Migre la base de données pour supporter le type EPARGNE"""

    db_path = os.path.join('instance', 'budget.db')

    if not os.path.exists(db_path):
        print(f"❌ Erreur : Base de données non trouvée à {db_path}")
        return False

    # Créer une sauvegarde de sécurité
    backup_path = f"{db_path}.pre_epargne_backup"
    import shutil
    shutil.copy2(db_path, backup_path)
    print(f"✅ Sauvegarde créée : {backup_path}")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Vérifier si la contrainte existe déjà
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='transactions'")
        current_schema = cursor.fetchone()[0]

        if "'EPARGNE'" in current_schema or '"EPARGNE"' in current_schema:
            print("✅ La contrainte EPARGNE existe déjà dans la base de données")
            conn.close()
            return True

        print("📝 Migration de la table transactions...")

        # Désactiver les foreign keys temporairement
        cursor.execute("PRAGMA foreign_keys=OFF")

        # Commencer une transaction
        cursor.execute("BEGIN TRANSACTION")

        # Supprimer l'index existant avant de renommer
        try:
            cursor.execute("DROP INDEX IF EXISTS idx_period_type")
            print("  → Index existant supprimé")
        except sqlite3.OperationalError:
            pass

        # Renommer l'ancienne table
        cursor.execute("ALTER TABLE transactions RENAME TO transactions_old")
        print("  → Table renommée en transactions_old")

        # Créer la nouvelle table avec la contrainte mise à jour
        cursor.execute("""
            CREATE TABLE transactions (
                id INTEGER NOT NULL PRIMARY KEY,
                period_id INTEGER NOT NULL,
                type VARCHAR(10) NOT NULL,
                amount NUMERIC(10, 2) NOT NULL,
                label VARCHAR(200) NOT NULL,
                category VARCHAR(100),
                notes TEXT,
                pointed BOOLEAN NOT NULL,
                created_at DATETIME,
                updated_at DATETIME,
                FOREIGN KEY(period_id) REFERENCES periods (id),
                CHECK (amount > 0),
                CHECK (type IN ('ENTREE', 'DEPENSE', 'EPARGNE'))
            )
        """)
        print("  → Nouvelle table créée avec contrainte EPARGNE")

        # Créer l'index (s'il n'existe pas déjà sur l'ancienne table)
        try:
            cursor.execute("CREATE INDEX idx_period_type ON transactions (period_id, type)")
            print("  → Index créé")
        except sqlite3.OperationalError:
            # L'index existe peut-être déjà, on continue
            print("  → Index déjà présent")

        # Copier toutes les données
        cursor.execute("""
            INSERT INTO transactions
            (id, period_id, type, amount, label, category, notes, pointed, created_at, updated_at)
            SELECT id, period_id, type, amount, label, category, notes, pointed, created_at, updated_at
            FROM transactions_old
        """)

        # Vérifier que toutes les données ont été copiées
        cursor.execute("SELECT COUNT(*) FROM transactions_old")
        old_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM transactions")
        new_count = cursor.fetchone()[0]

        if old_count != new_count:
            raise Exception(f"Erreur : {old_count} transactions dans l'ancienne table, {new_count} dans la nouvelle")

        print(f"  → {new_count} transactions copiées")

        # Supprimer l'ancienne table
        cursor.execute("DROP TABLE transactions_old")
        print("  → Ancienne table supprimée")

        # Valider la transaction
        conn.commit()
        print("  → Transaction validée")

        # Réactiver les foreign keys
        cursor.execute("PRAGMA foreign_keys=ON")

        # Vérifier l'intégrité de la base de données
        cursor.execute("PRAGMA integrity_check")
        integrity = cursor.fetchone()[0]
        if integrity != 'ok':
            raise Exception(f"Erreur d'intégrité : {integrity}")

        print("  → Vérification d'intégrité : OK")

        conn.close()

        print("\n✅ Migration réussie !")
        print(f"   - {new_count} transactions migrées")
        print(f"   - Type EPARGNE maintenant supporté")
        print(f"   - Sauvegarde disponible : {backup_path}")

        return True

    except Exception as e:
        print(f"\n❌ Erreur lors de la migration : {e}")
        print(f"   La base de données n'a pas été modifiée")
        print(f"   Sauvegarde disponible : {backup_path}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    print("=== Migration EPARGNE ===\n")
    success = migrate_database()

    if success:
        print("\n🎉 Vous pouvez maintenant créer des transactions d'épargne !")
        print("   Redémarrez votre application Flask pour utiliser la nouvelle base de données.")
    else:
        print("\n⚠️  La migration a échoué. Votre base de données n'a pas été modifiée.")
