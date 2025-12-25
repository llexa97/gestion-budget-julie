# Guide de migration - Suppression du champ date et ajout du pointage

## Changements apportés

Cette mise à jour modifie le modèle `Transaction` :
- ✅ **Suppression** du champ `date` (plus nécessaire)
- ✅ **Ajout** du champ `pointed` (booléen pour pointer les transactions)
- ✅ Ajout d'une interface de pointage avec cases à cocher
- ✅ Suppression du champ date dans le formulaire de création/modification

## Migration de la base de données en production

### ⚠️ IMPORTANT : Sauvegarde

**Avant toute manipulation, faites une sauvegarde de votre base de données !**

```bash
# Sur votre serveur de production
cp instance/budget.db instance/budget.db.backup-$(date +%Y%m%d)
```

### Étape 1 : Déployer le nouveau code

```bash
# Sur votre serveur de production
git pull origin main  # ou la branche appropriée
```

### Étape 2 : Activer l'environnement virtuel

```bash
source venv/bin/activate  # ou le chemin de votre venv
```

### Étape 3 : Appliquer la migration

```bash
flask db upgrade
```

Cette commande va :
1. Ajouter la colonne `pointed` à toutes les transactions existantes (valeur par défaut : False)
2. Supprimer la colonne `date`
3. Supprimer l'index `idx_period_date`

### Étape 4 : Redémarrer l'application

```bash
# Si vous utilisez systemd
sudo systemctl restart budget-manager

# Ou avec gunicorn directement
pkill gunicorn
gunicorn --bind 0.0.0.0:5001 wsgi:app
```

### Étape 5 : Vérifier

1. Accédez à votre application
2. Vérifiez qu'une colonne "Pointé" apparaît dans la liste des transactions
3. Testez le pointage en cliquant sur les cases à cocher
4. Créez une nouvelle transaction pour vérifier que le formulaire n'a plus de champ date

## En cas de problème

### Annuler la migration

Si quelque chose ne fonctionne pas, vous pouvez revenir en arrière :

```bash
flask db downgrade
```

Cela va :
1. Réajouter la colonne `date` (avec une valeur par défaut 2025-01-01 pour les anciennes transactions)
2. Supprimer la colonne `pointed`
3. Recréer l'index `idx_period_date`

### Restaurer la sauvegarde

Si nécessaire, restaurez votre sauvegarde :

```bash
cp instance/budget.db.backup-YYYYMMDD instance/budget.db
sudo systemctl restart budget-manager
```

## Développement local

Si vous voulez tester en local d'abord :

```bash
# Cloner votre base de données de prod
scp user@serveur:/path/to/instance/budget.db instance/budget.db

# Appliquer la migration
source .venv/bin/activate
flask db upgrade

# Tester l'application
python main.py
```

## Fichiers de migration

La migration se trouve dans :
```
migrations/versions/0e9c474e3c9c_remove_date_field_and_add_pointed_field_.py
```

## Support

En cas de problème lors de la migration, vérifiez :
- Les logs de l'application
- Les erreurs de la commande `flask db upgrade`
- La structure de la base de données avec `sqlite3 instance/budget.db ".schema transactions"`
