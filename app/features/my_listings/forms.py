# app/features/my_listings/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class EditItemForm(FlaskForm):
    title = StringField('Item Name', validators=[DataRequired(), Length(max=255)])  # Changed 'name' to 'title'
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('electronics', 'Electronics'),
        ('books', 'Books'),
        ('keys', 'Keys'),
        ('clothing', 'Clothing'),
        ('id_cards', 'ID Cards'),  # Added ID Cards
        ('other', 'Other')
    ], validators=[DataRequired()])  # Added DataRequired validator
    campus = SelectField('Campus', choices=[
        ('Steve Biko Campus', 'Steve Biko Campus'),
        ('ML Sultan Campus', 'ML Sultan Campus'),
        ('Ritson Campus', 'Ritson Campus')
    ], validators=[DataRequired()])  # Added campus field and DataRequired
    location_found = StringField('Location Found', validators=[DataRequired(), Length(max=255)]) # Changed 'location' to 'location_found'
    submit = SubmitField('Update Item')