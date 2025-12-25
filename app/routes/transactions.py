from flask import Blueprint, render_template, redirect, url_for, flash, request
import logging

from app import db
from app.models import Transaction, Period
from app.forms import TransactionForm

bp = Blueprint('transactions', __name__, url_prefix='/transactions')

# Configuration du logger
logger = logging.getLogger(__name__)


@bp.route('/create/<int:period_id>', methods=['GET', 'POST'])
def create(period_id):
    """Créer une nouvelle transaction pour une période"""
    logger.info(f"📝 [CREATE] Début création transaction pour période {period_id}")
    logger.info(f"📝 [CREATE] Méthode: {request.method}")

    period = Period.query.get_or_404(period_id)
    logger.info(f"📝 [CREATE] Période trouvée: {period.get_formatted_period()}")

    form = TransactionForm()

    # Pré-remplir le type si passé en paramètre
    if request.method == 'GET' and request.args.get('type'):
        form.type.data = request.args.get('type')
        logger.info(f"📝 [CREATE] Type pré-rempli: {form.type.data}")

    if form.validate_on_submit():
        logger.info(f"📝 [CREATE] Formulaire validé avec succès")
        logger.info(f"📝 [CREATE] Données du formulaire:")
        logger.info(f"  - Type: {form.type.data}")
        logger.info(f"  - Amount: {form.amount.data}")
        logger.info(f"  - Label: {form.label.data}")
        logger.info(f"  - Category: {form.category.data}")
        logger.info(f"  - Notes: {form.notes.data}")

        transaction = Transaction(
            period_id=period_id,
            type=form.type.data,
            amount=form.amount.data,
            label=form.label.data,
            category=form.category.data,
            notes=form.notes.data,
            pointed=False
        )
        logger.info(f"📝 [CREATE] Objet Transaction créé")

        try:
            logger.info(f"📝 [CREATE] Tentative d'ajout à la session DB")
            db.session.add(transaction)
            logger.info(f"📝 [CREATE] Transaction ajoutée à la session, tentative de commit")
            db.session.commit()
            logger.info(f"✅ [CREATE] Transaction créée avec succès - ID: {transaction.id}")
            flash(f'Transaction "{transaction.label}" ajoutée avec succès', 'success')
            return redirect(url_for('periods.detail', period_id=period_id))
        except Exception as e:
            logger.error(f"❌ [CREATE] Erreur lors de la création: {type(e).__name__}")
            logger.error(f"❌ [CREATE] Message d'erreur: {str(e)}")
            logger.error(f"❌ [CREATE] Détails complets:", exc_info=True)
            db.session.rollback()
            flash(f'Erreur lors de la création de la transaction: {str(e)}', 'error')
    else:
        if request.method == 'POST':
            logger.warning(f"⚠️  [CREATE] Formulaire invalide")
            logger.warning(f"⚠️  [CREATE] Erreurs de validation: {form.errors}")

    return render_template('transactions/form.html', form=form, period=period, action='create')


@bp.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def edit(transaction_id):
    """Modifier une transaction existante"""
    transaction = Transaction.query.get_or_404(transaction_id)
    period = transaction.period
    form = TransactionForm(obj=transaction)

    if form.validate_on_submit():
        transaction.type = form.type.data
        transaction.amount = form.amount.data
        transaction.label = form.label.data
        transaction.category = form.category.data
        transaction.notes = form.notes.data

        try:
            db.session.commit()
            flash(f'Transaction "{transaction.label}" modifiée avec succès', 'success')
            return redirect(url_for('periods.detail', period_id=period.id))
        except Exception as e:
            db.session.rollback()
            flash('Erreur lors de la modification de la transaction', 'error')

    return render_template('transactions/form.html', form=form, period=period, action='edit')


@bp.route('/delete/<int:transaction_id>', methods=['POST'])
def delete(transaction_id):
    """Supprimer une transaction"""
    transaction = Transaction.query.get_or_404(transaction_id)
    period_id = transaction.period_id

    try:
        db.session.delete(transaction)
        db.session.commit()
        flash(f'Transaction "{transaction.label}" supprimée avec succès', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erreur lors de la suppression de la transaction', 'error')

    return redirect(url_for('periods.detail', period_id=period_id))


@bp.route('/toggle-pointed/<int:transaction_id>', methods=['POST'])
def toggle_pointed(transaction_id):
    """Basculer le statut pointé d'une transaction"""
    transaction = Transaction.query.get_or_404(transaction_id)
    period_id = transaction.period_id

    try:
        transaction.pointed = not transaction.pointed
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('Erreur lors de la mise à jour du pointage', 'error')

    return redirect(url_for('periods.detail', period_id=period_id))
