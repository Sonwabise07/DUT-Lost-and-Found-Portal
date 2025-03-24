from datetime import datetime
from app import db  # Import your database instance

class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    agreement_text = db.Column(db.Text, nullable=False)  # Store the FULL agreement text
    agreement_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    claim_status = db.Column(db.String(20), nullable=False, default='pending')  # 'pending', 'approved', 'rejected', 'investigation'

    user = db.relationship('User', backref=db.backref('claims', lazy=True))
    item = db.relationship('Item', backref=db.backref('claims', lazy=True))

    def __repr__(self):
        return f'<Claim {self.id} for Item {self.item_id} by User {self.user_id}>'