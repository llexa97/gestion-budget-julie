# Application de Gestion de Budget Mensuel

Application web Flask pour gérer vos finances personnelles mois par mois.

## Fonctionnalités

- Création et gestion de périodes mensuelles
- Suivi des entrées d'argent (revenus)
- Suivi des dépenses
- Calcul automatique du solde mensuel
- Filtrage et recherche de transactions
- Interface responsive et intuitive

## Structure du projet

```
.
├── app/
│   ├── __init__.py           # Factory Flask
│   ├── models.py             # Modèles SQLAlchemy (Period, Transaction)
│   ├── forms.py              # Formulaires Flask-WTF
│   ├── routes/
│   │   ├── periods.py        # Routes pour les périodes
│   │   └── transactions.py   # Routes pour les transactions
│   ├── templates/            # Templates Jinja2
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── periods/
│   │   └── transactions/
│   └── static/               # Fichiers CSS et JS
│       ├── css/
│       └── js/
├── tests/                    # Tests unitaires
├── instance/                 # Base de données SQLite (créée automatiquement)
├── config.py                 # Configuration de l'application
├── main.py                   # Point d'entrée
├── pyproject.toml            # Dépendances
└── PRD.md                    # Document de spécifications

```

## Installation

### Prérequis

- Python 3.12 ou supérieur
- uv (recommandé) ou pip pour la gestion des dépendances

### Étapes d'installation avec uv (recommandé)

1. Installer uv si ce n'est pas déjà fait :
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Créer l'environnement virtuel et installer les dépendances :
```bash
uv venv
uv pip install -e .
```

3. Initialiser la base de données :
```bash
uv run python -c "from main import app; from app import db; app.app_context().push(); db.create_all()"
```

### Alternative avec pip

1. Créer un environnement virtuel :
```bash
python -m venv .venv
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate
```

2. Installer les dépendances :
```bash
pip install -e .
```

3. Initialiser la base de données :
```bash
python -c "from main import app; from app import db; app.app_context().push(); db.create_all()"
```

### Avec Flask-Migrate (optionnel)

```bash
uv run flask db init
uv run flask db migrate -m "Initial migration"
uv run flask db upgrade
```

## Démarrage de l'application

### Avec uv (recommandé)

```bash
uv run python main.py
```

### Mode développement classique

```bash
source .venv/bin/activate  # Activer l'environnement virtuel
python main.py
```

L'application sera accessible sur http://localhost:5000

### Avec Flask CLI

```bash
export FLASK_APP=main.py
export FLASK_ENV=development
uv run flask run
```

## Utilisation

1. **Créer une période** : Accédez au dashboard et cliquez sur "Créer une période"
2. **Ajouter des transactions** : Dans le détail d'une période, ajoutez des entrées et des dépenses
3. **Consulter le bilan** : Les totaux sont calculés automatiquement
4. **Filtrer et rechercher** : Utilisez les filtres pour retrouver vos transactions

## Développement

### Installer les dépendances de développement

```bash
uv pip install -e ".[dev]"
```

### Lancer les tests

```bash
uv run pytest
```

### Formatage du code

```bash
uv run black .
```

### Linting

```bash
uv run flake8
```

## Configuration

La configuration se trouve dans `config.py`. Vous pouvez :

- Définir une clé secrète via la variable d'environnement `SECRET_KEY`
- Changer l'URI de la base de données via `DATABASE_URL`
- Basculer entre les modes development, production, et test

## Technologies utilisées

- **Flask** : Framework web
- **SQLAlchemy** : ORM pour la base de données
- **Flask-Migrate** : Migrations de base de données
- **Flask-WTF** : Formulaires et protection CSRF
- **SQLite** : Base de données (par défaut)

## Prochaines fonctionnalités (V1.1)

- Export CSV des transactions
- Graphiques de répartition des dépenses
- Catégories personnalisables
- Comparaison entre périodes

## Licence

Ce projet est un outil personnel de gestion de budget.
