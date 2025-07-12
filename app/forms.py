# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import re

class RegistrationForm(FlaskForm):
    """
    Form for user registration.
    Validates user input for first name, last name, email, campus, and password.
    """
    
    # First Name Field
    first_name = StringField('First Name', 
                             validators=[DataRequired(message="First name is required.")])
    
    # Last Name Field
    last_name = StringField('Last Name', 
                            validators=[DataRequired(message="Last name is required.")])
    
    # Email Address Field
    email = StringField('Email', 
                        validators=[DataRequired(message="Email is required."), Email(message="Please enter a valid email address.")])
    
    # Campus Selection Dropdown
    campus = SelectField('Campus', 
                         choices=[
                             ('', '--- Select a Campus ---'), # Placeholder option
                             ('Ritson', 'Ritson'), 
                             ('Ml Sultan', 'Ml Sultan'), 
                             ('Steve Biko', 'Steve Biko'), 
                             ('City Campus', 'City Campus')
                         ],
                         validators=[DataRequired(message="Please select your campus.")])
    
    # Password Field
    password = PasswordField('Password', 
                             validators=[DataRequired(message="Password is required."), Length(min=8)])
    
    # Confirm Password Field
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[
                                         DataRequired(message="Please confirm your password."), 
                                         EqualTo('password', message='Passwords must match.')
                                     ])
    
    # Submit Button
    submit = SubmitField('Register')

    def validate_password(self, password):
        """
        Custom validator for password complexity.
        Ensures the password meets the required criteria.
        """
        p = re.compile(r'(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}')
        if not p.match(password.data):
            # Create a more user-friendly error message
            error_message = """
            Password must contain at least:
            <ul>
                <li>8 characters</li>
                <li>One uppercase letter (A-Z)</li>
                <li>One lowercase letter (a-z)</li>
                <li>One number (0-9)</li>
                <li>One special character (@$!%*?&)</li>
            </ul>
            """
            raise ValidationError(error_message)