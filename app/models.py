from datetime import datetime
from decimal import Decimal
from enum import Enum

from app import db


class TransactionType(Enum):
    """Type de transaction"""
    ENTREE = "ENTREE"
    DEPENSE = "DEPENSE"
    EPARGNE = "EPARGNE"


class Period(db.Model):
    """Modèle pour une période mensuelle"""
    __tablename__ = 'periods'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    transactions = db.relationship('Transaction', back_populates='period', cascade='all, delete-orphan')

    # Contrainte d'unicité sur (year, month)
    __table_args__ = (
        db.UniqueConstraint('year', 'month', name='unique_year_month'),
        db.CheckConstraint('month >= 1 AND month <= 12', name='valid_month'),
        db.CheckConstraint('year >= 2000 AND year <= 2100', name='valid_year'),
    )

    def __repr__(self):
        return f'<Period {self.year}-{self.month:02d}>'

    def get_month_name(self):
        """Retourne le nom du mois en français"""
        months = {
            1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril',
            5: 'Mai', 6: 'Juin', 7: 'Juillet', 8: 'Août',
            9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
        }
        return months.get(self.month, '')

    def get_formatted_period(self):
        """Retourne la période au format 'Mois Année'"""
        return f"{self.get_month_name()} {self.year}"

    def get_total_entrees(self):
        """Calcule le total des entrées pour cette période"""
        return sum(
            t.amount for t in self.transactions
            if t.type == TransactionType.ENTREE.value
        ) or Decimal('0.00')

    def get_total_depenses(self):
        """Calcule le total des dépenses pour cette période"""
        return sum(
            t.amount for t in self.transactions
            if t.type == TransactionType.DEPENSE.value
        ) or Decimal('0.00')

    def get_total_epargne(self):
        """Calcule le total de l'épargne pour cette période"""
        return sum(
            t.amount for t in self.transactions
            if t.type == TransactionType.EPARGNE.value
        ) or Decimal('0.00')

    def get_resultat(self):
        """Calcule le résultat (entrées - dépenses - épargne)"""
        return self.get_total_entrees() - self.get_total_depenses() - self.get_total_epargne()


class Transaction(db.Model):
    """Modèle pour une transaction (entrée ou dépense)"""
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column(db.Integer, db.ForeignKey('periods.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    label = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    pointed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    period = db.relationship('Period', back_populates='transactions')

    # Contraintes
    __table_args__ = (
        db.CheckConstraint('amount >= 0', name='positive_amount'),
        db.CheckConstraint("type IN ('ENTREE', 'DEPENSE', 'EPARGNE')", name='valid_type'),
        db.Index('idx_period_type', 'period_id', 'type'),
    )

    def __repr__(self):
        return f'<Transaction {self.type} {self.amount} - {self.label}>'
