from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import Email, InputRequired, Length, URL


class RestaurantForm(FlaskForm):
    """Create WTForm to add restaurants"""
    name = StringField('Name', validators=[InputRequired()])
    phone = StringField('Phone #', validators=[InputRequired()])
    email = StringField('E-Mail', validators=[InputRequired(),
                                              Email("This field requires a valid email address")])
    course = SelectField(u'Course', choices=[('American', 'American'), ('Mexican', 'Mexican'),
                                             ('India', 'India'), ('Mediterranean', 'Mediterranean'),
                                             ('Caribbean', 'Caribbean'), ('Asia', 'Asia'),
                                             ('Mix', 'Mix')], validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired(), Length(min=5, max=200)])
    website = StringField('Website', validators=[InputRequired(),
                                                 URL(require_tld=True, message="Enter a valid URL")])
    street = StringField('Street', validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired()])
    state = StringField('State', validators=[InputRequired()])
    zip_code = StringField('Zip Code', validators=[InputRequired()])
