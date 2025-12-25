from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Length


class PeriodForm(FlaskForm):
    """Formulaire pour créer/modifier une période"""
    year = SelectField('Année', coerce=int, validators=[DataRequired()])
    month = SelectField('Mois', coerce=int, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(PeriodForm, self).__init__(*args, **kwargs)
        # Générer les années de 2020 à 2030
        current_year = date.today().year
        self.year.choices = [(y, str(y)) for y in range(current_year - 5, current_year + 6)]
        # Mois
        self.month.choices = [
            (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
            (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
            (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
        ]


class TransactionForm(FlaskForm):
    """Formulaire pour créer/modifier une transaction"""
    type = SelectField(
        'Type',
        choices=[('ENTREE', 'Entrée'), ('DEPENSE', 'Dépense'), ('EPARGNE', 'Épargne')],
        validators=[DataRequired()]
    )
    amount = DecimalField(
        'Montant',
        validators=[
            InputRequired(message='Le montant est obligatoire'),
            NumberRange(min=0, message='Le montant doit être supérieur ou égal à 0')
        ],
        places=2
    )
    label = StringField(
        'Libellé',
        validators=[
            DataRequired(message='Le libellé est obligatoire'),
            Length(max=200, message='Le libellé ne peut pas dépasser 200 caractères')
        ]
    )
    category = StringField(
        'Catégorie (optionnel)',
        validators=[Length(max=100)]
    )
    notes = TextAreaField(
        'Notes (optionnel)'
    )
