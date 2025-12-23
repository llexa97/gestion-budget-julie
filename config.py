import os
from pathlib import Path

basedir = Path(__file__).parent


class Config:
    """Configuration de base pour l'application Flask"""

    # Clé secrète pour les sessions et CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Configuration de la base de données
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{basedir / "instance" / "budget.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuration WTForms
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True


class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False


class TestConfig(Config):
    """Configuration pour les tests"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig,
    'default': DevelopmentConfig
}
