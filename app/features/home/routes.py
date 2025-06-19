from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.models.item import Item
from app.features.home import home_bp  # Import the blueprint
from datetime import datetime, timedelta, date
from sqlalchemy import and_, func

# home_bp = Blueprint('home', __name__, template_folder='templates') # REMOVE THIS - It's already in __init__.py

@home_bp.route('/')
def index():
    return redirect(url_for('home.home'))

@home_bp.route("/home")
def home():
    recent_listings = Item.query.filter(Item.returned == False).order_by(Item.date_reported.desc()).limit(10).all()
    return render_template('home.html', recent_listings=recent_listings)  # Correct path

@home_bp.route('/search', methods=['GET'])
def search_items():
    search_term = request.args.get('search', '')
    campus_filter = request.args.get('campus', 'all')
    date_filter_str = request.args.get('date', '')
    category_filter = request.args.get('category', 'all')

    print(f"*** Search Term: {search_term}")
    print(f"*** Campus Filter: {campus_filter}")
    print(f"*** Date Filter (str): {date_filter_str}")
    print(f"*** Category Filter: {category_filter}")

    query = Item.query.filter(Item.returned == False)

    if search_term:
        query = query.filter(db.or_(Item.title.ilike(f"%{search_term}%"),
                                    Item.description.ilike(f"%{search_term}%")))
        print("*** Search Term Filter Applied")

    if campus_filter != 'all':
        query = query.filter(Item.campus == campus_filter)
        print(f"*** Campus Filter Applied: {campus_filter}")

    if date_filter_str:
        try:
            date_obj = datetime.strptime(date_filter_str, '%Y-%m-%d').date()
            print(f"*** Date Object Parsed: {date_obj}")

            query = query.filter(func.DATE(Item.date_reported) == date_obj)
            print("*** Date Filter Applied")

        except ValueError as e:
            print(f"*** Date Parsing Error: {e}")
            flash("Invalid date format.  Please useரும்பு-MM-DD.", 'error')

    if category_filter != 'all':
        if category_filter == 'id_cards':
            query = query.filter(func.lower(Item.category) == 'id_cards')
            print("*** ID Cards Category Filter Applied")
        else:
            query = query.filter(func.lower(Item.category) == category_filter.lower())
            print(f"*** Category Filter Applied (Non-ID Cards): {category_filter}")

    items = query.all()
    print(f"*** Found items: {items}")

    return render_template('search_items.html', items=items, search_term=search_term,
                            category_filter=category_filter, campus_filter=campus_filter,
                            date_filter=date_filter_str)

@home_bp.route('/item/<int:item_id>')
@login_required
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('item_detail.html', item=item)  # Correct path