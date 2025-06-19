# app/features/admin/forms.py
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class ClaimApprovalForm(FlaskForm):
    status = SelectField('Status',
                         choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
                         validators=[DataRequired()])
    submit = SubmitField('Update Status')