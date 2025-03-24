from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, FileField, TelField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, Email


class ReportForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(message="Please enter a title for the item."),
        Length(max=100, message="Title must be less than 100 characters.")
    ])

    description = TextAreaField('Description', validators=[
        DataRequired(message="Please describe the item and where you found it."),
        Length(max=500, message="Description must be less than 500 characters.")
    ])
    category = SelectField('Category', choices=[
        ('electronics', 'Electronics'),
        ('id_cards', 'ID Cards'),
        ('books', 'Books'),
        ('clothing', 'Clothing'),
        ('bags & wallets', 'Bags & Wallets'),
        ('keys', 'Keys'),
        ('student cards/id', 'Student Cards/ID'),
        ('jewelry', 'Jewelry'),
        ('others', 'Others')
    ], validators=[DataRequired(message = "Please select a category")])
    other_category = StringField('If other, specify:')  # No validators here!

    campus = SelectField('Campus', choices=[
        ('Ritson Campus', 'Ritson Campus'),
        ('Steve Biko Campus', 'Steve Biko Campus'),
        ('ML Sultan Campus', 'ML Sultan Campus'),
        ('City Campus', 'City Campus'),
        ('Other', 'Other')
    ], validators=[DataRequired(message="Please select a campus.")])
    other_location = StringField('If other, specify:')  # No validators here!

    location_found = StringField('Location Found', validators=[DataRequired(message="Please enter the location where the item was found.")])
    image = FileField('Image')
    privacy_consent = BooleanField('I consent to my contact information being shared with the owner of the item.', validators=[DataRequired(message="You must consent to share your contact information.")])

    contact_method = SelectField('Preferred Contact Method', choices=[
        ('', 'Select a contact method'),  # Add an empty option
        ('call', 'Phone Call'),
        ('whatsapp', 'WhatsApp'),
        ('social_media', 'Social Media'),
        ('email', 'Email')
    ], validators=[DataRequired(message="Please select how you want to be contacted.")])

    phone_number = TelField('Phone Number', validators= [Optional()])
    whatsapp_number = TelField('WhatsApp Number', validators=[Optional()])  # Use TelField
    social_media_handle = StringField('Social Media Handle', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email(message="Please enter a valid email address.")])

    submit = SubmitField('Submit Report')