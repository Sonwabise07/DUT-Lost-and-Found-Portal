# app/features/my_listings/routes.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.item import Item

my_listings_bp = Blueprint('my_listings', __name__, template_folder='templates')

@my_listings_bp.route('/my_listings')
@login_required  # Important: Only logged-in users can see their listings
def my_listings():
    items = Item.query.filter_by(user_id=current_user.id).all()  # Fetch items by user_id
    return render_template('my_listings.html', items=items)