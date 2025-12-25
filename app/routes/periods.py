from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Period, Transaction
from app.forms import PeriodForm

bp = Blueprint('periods', __name__, url_prefix='/periods')


def index():
    """Page d'accueil - Dashboard avec liste des périodes"""
    periods = Period.query.order_by(Period.year.desc(), Period.month.desc()).all()
    return render_template('dashboard.html', periods=periods)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Créer une nouvelle période"""
    form = PeriodForm()

    if form.validate_on_submit():
        period = Period(
            year=form.year.data,
            month=form.month.data
        )

        try:
            db.session.add(period)
            db.session.commit()
            flash(f'Période {period.month:02d}/{period.year} créée avec succès', 'success')
            return redirect(url_for('periods.detail', period_id=period.id))
        except IntegrityError:
            db.session.rollback()
            flash(f'La période {form.month.data:02d}/{form.year.data} existe déjà', 'error')

    return render_template('periods/create.html', form=form)


@bp.route('/<int:period_id>')
def detail(period_id):
    """Afficher le détail d'une période avec ses transactions"""
    period = Period.query.get_or_404(period_id)

    # Filtres et tri
    transaction_type = request.args.get('type', '')
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort', 'created')
    sort_order = request.args.get('order', 'desc')

    # Query de base
    query = Transaction.query.filter_by(period_id=period_id)

    # Appliquer les filtres
    if transaction_type:
        query = query.filter_by(type=transaction_type)
    if search_query:
        query = query.filter(Transaction.label.ilike(f'%{search_query}%'))

    # Appliquer le tri
    if sort_by == 'amount':
        order_column = Transaction.amount
    elif sort_by == 'label':
        order_column = Transaction.label
    elif sort_by == 'pointed':
        order_column = Transaction.pointed
    elif sort_by == 'created':
        order_column = Transaction.id
    else:
        order_column = Transaction.id

    if sort_order == 'desc':
        query = query.order_by(order_column.desc())
    else:
        query = query.order_by(order_column.asc())

    transactions = query.all()

    return render_template(
        'periods/detail.html',
        period=period,
        transactions=transactions,
        filters={'type': transaction_type, 'search': search_query},
        sort={'by': sort_by, 'order': sort_order}
    )


@bp.route('/<int:period_id>/delete', methods=['POST'])
def delete(period_id):
    """Supprimer une période et toutes ses transactions"""
    period = Period.query.get_or_404(period_id)

    try:
        db.session.delete(period)
        db.session.commit()
        flash(f'Période {period.month:02d}/{period.year} supprimée avec succès', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erreur lors de la suppression de la période', 'error')

    return redirect(url_for('index'))
