from app import db  # Import db from the app package
from datetime import datetime
from flask import url_for

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    campus = db.Column(db.String(50), nullable=False)
    location_found = db.Column(db.String(100), nullable=False)
    date_found = db.Column(db.Date, nullable=False)  # Date only
    time_found = db.Column(db.Time) # Time only
    image_filename = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_reported = db.Column(db.DateTime, default=datetime.utcnow)
    # adding contact information
    contact_method = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))  # Adjust length as needed
    whatsapp_number = db.Column(db.String(20)) # Adjust length as needed
    social_media = db.Column(db.String(100))  # Adjust length as needed
    email = db.Column(db.String(120))

    # Relationship (Corrected)
    reporter = db.relationship('User', lazy=True) # Keep.

    def __repr__(self):
        return f"<Item {self.title}>"

    @property
    def image_url(self):
        if self.image_filename:
            return url_for('static', filename=f'uploads/{self.image_filename}')  # Correct URL
        return url_for('static', filename='uploads/default.jpg')  # Provide a default