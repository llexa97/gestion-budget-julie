from flask import Blueprint, render_template, redirect, url_for, flash, request
from datetime import date

from app import db
from app.models import Transaction, Period
from app.forms import TransactionForm

bp = Blueprint('transactions', __name__, url_prefix='/transactions')


@bp.route('/create/<int:period_id>', methods=['GET', 'POST'])
def create(period_id):
    """Créer une nouvelle transaction pour une période"""
    period = Period.query.get_or_404(period_id)
    form = TransactionForm()

    # Pré-remplir le type si passé en paramètre
    if request.method == 'GET' and request.args.get('type'):
        form.type.data = request.args.get('type')

    if form.validate_on_submit():
        # Validation optionnelle : vérifier que la date est dans le mois de la période
        transaction_date = form.date.data
        if transaction_date.year != period.year or transaction_date.month != period.month:
            flash(
                f'Attention : la date de la transaction ({transaction_date.strftime("%d/%m/%Y")}) '
                f'ne correspond pas au mois de la période ({period.month:02d}/{period.year})',
                'warning'
            )

        transaction = Transaction(
            period_id=period_id,
            type=form.type.data,
            amount=form.amount.data,
            date=form.date.data,
            label=form.label.data,
            category=form.category.data,
            notes=form.notes.data
        )

        try:
            db.session.add(transaction)
            db.session.commit()
            flash(f'Transaction "{transaction.label}" ajoutée avec succès', 'success')
            return redirect(url_for('periods.detail', period_id=period_id))
        except Exception as e:
            db.session.rollback()
            flash('Erreur lors de la création de la transaction', 'error')

    return render_template('transactions/form.html', form=form, period=period, action='create')


@bp.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def edit(transaction_id):
    """Modifier une transaction existante"""
    transaction = Transaction.query.get_or_404(transaction_id)
    period = transaction.period
    form = TransactionForm(obj=transaction)

    if form.validate_on_submit():
        # Validation optionnelle : vérifier que la date est dans le mois de la période
        transaction_date = form.date.data
        if transaction_date.year != period.year or transaction_date.month != period.month:
            flash(
                f'Attention : la date de la transaction ({transaction_date.strftime("%d/%m/%Y")}) '
                f'ne correspond pas au mois de la période ({period.month:02d}/{period.year})',
                'warning'
            )

        transaction.type = form.type.data
        transaction.amount = form.amount.data
        transaction.date = form.date.data
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
