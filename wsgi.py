"""
Point d'entrée WSGI pour l'application Budget Manager

Ce fichier est utilisé par les serveurs WSGI (Gunicorn, uWSGI, etc.)
pour servir l'application Flask en production.

Usage avec Gunicorn:
    gunicorn -w 4 -b 0.0.0.0:5001 wsgi:app

Usage avec uWSGI:
    uwsgi --http :5001 --wsgi-file wsgi.py --callable app
"""

import os
from app import create_app, db
from app.models import Period, Transaction

# Créer l'application Flask
app = create_app(os.getenv('FLASK_ENV', 'production'))


@app.shell_context_processor
def make_shell_context():
    """Rendre les modèles disponibles dans le shell Flask"""
    return {
        'db': db,
        'Period': Period,
        'Transaction': Transaction
    }


if __name__ == "__main__":
    # Ce bloc n'est exécuté que si le fichier est lancé directement
    # (pas recommandé en production, utiliser Gunicorn à la place)
    app.run()
