from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app import db
from app.models.item import Item
from flask import Blueprint
from datetime import datetime, timedelta

home_bp = Blueprint('home', __name__, template_folder='templates')


@home_bp.route('/')
def index():
    print("*** Inside the index route!")  # CONFIRM EXECUTION
    return redirect(url_for('home.home'))

@home_bp.route("/home")
def home():
    search_term = request.args.get('search', '')
    campus_filter = request.args.get('campus', 'all')
    date_filter = request.args.get('date', 'all')
    category_filter = request.args.get('category', 'all')

    query = Item.query

    if search_term:
        query = query.filter(Item.title.ilike(f"%{search_term}%"))
    if campus_filter != 'all':
        query = query.filter_by(campus=campus_filter)
    if date_filter != 'all':
        if date_filter == 'today':
            query = query.filter(Item.date_found == datetime.today().date())
        elif date_filter == 'week':
            query = query.filter(Item.date_found >= datetime.today().date() - timedelta(days=7) )
        elif date_filter == 'month':
            query = query.filter(Item.date_found >= datetime.today().date() - timedelta(days=30))
    if category_filter != 'all':
        query = query.filter_by(category=category_filter)

    items = query.all()
    recent_listings = items[-10:]

    return render_template('home.html',
                            recent_listings=recent_listings,
                            search_term=search_term,
                            campus_filter=campus_filter,
                            date_filter=date_filter,
                            category_filter=category_filter)