#!/usr/bin/env python3
"""
Script pour ajouter manuellement la colonne 'pointed' à la table transactions
"""
from app import create_app, db

def add_pointed_column():
    app = create_app()

    with app.app_context():
        print("🔍 Vérification de la colonne 'pointed'...")

        try:
            # Tenter d'ajouter la colonne pointed
            with db.engine.begin() as connection:
                connection.execute(db.text("ALTER TABLE transactions ADD COLUMN pointed BOOLEAN DEFAULT 0 NOT NULL"))
            print("✅ Colonne 'pointed' ajoutée avec succès!")
            return True

        except Exception as e:
            error_msg = str(e).lower()
            if "duplicate column" in error_msg or "already exists" in error_msg:
                print("ℹ️  La colonne 'pointed' existe déjà dans la base de données")
                return True
            else:
                print(f"❌ Erreur lors de l'ajout de la colonne: {e}")
                return False

if __name__ == "__main__":
    print("=" * 60)
    print("  Script d'ajout de la colonne 'pointed'")
    print("=" * 60)
    print()

    success = add_pointed_column()

    print()
    if success:
        print("✅ Opération terminée avec succès!")
        print("👉 Redémarrez maintenant le service avec:")
        print("   sudo systemctl restart budget-manager")
    else:
        print("❌ Échec de l'opération")
        print("👉 Contactez le support pour obtenir de l'aide")
    print()
