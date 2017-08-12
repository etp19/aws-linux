from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import InputRequired


class MenuItems(FlaskForm):
    """Create WTForm to add Menu Items"""
    name = StringField('Item Name', validators=[InputRequired()])
    price = StringField('Price', validators=[InputRequired()])
    course = SelectField(u'Course', choices=[('Appetizer', 'Appetizer'), ('Entree', 'Entree'),
                                             ('Dessert', 'Dessert'), ('Beverage', 'Beverage'),
                                             ], validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
