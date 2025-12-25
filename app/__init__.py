from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import sys

from config import config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='default'):
    """Factory pattern pour créer l'application Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Configuration du logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    app.logger.setLevel(logging.INFO)
    app.logger.info("🚀 Application Budget Manager démarrée")

    # Initialiser les extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Enregistrer les blueprints
    from app.routes import periods, transactions
    app.register_blueprint(periods.bp)
    app.register_blueprint(transactions.bp)

    # Route principale (dashboard)
    from app.routes.periods import index
    app.add_url_rule('/', 'index', index)

    # Initialiser la base de données automatiquement
    with app.app_context():
        db.create_all()

    return app
