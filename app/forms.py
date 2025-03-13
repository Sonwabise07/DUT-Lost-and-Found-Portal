# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import re

class RegistrationForm(FlaskForm):
    # First Name
    first_name = StringField('First Name', validators=[DataRequired()])
    
    # Last Name
    last_name = StringField('Last Name', validators=[DataRequired()])
    
    # Email Address
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    # Campus Selection
    campus = SelectField('Campus', choices=[('Ritson', 'Ritson'), ('Ml Sultan', 'Ml Sultan'), 
                                            ('Steve Biko', 'Steve Biko'), ('City Campus', 'City Campus')],
                                validators=[DataRequired()])
    
    # Password Field
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    
    # Confirm Password Field
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    def validate_password(self, password):
        p = re.compile(r'(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}')
        if not p.match(password.data):
            raise ValidationError("Password must contain at least 8 characters, including uppercase, lowercase, numbers, and special characters.")