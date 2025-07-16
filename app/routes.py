from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db  # Import app from __init__.py
from app.models import User, Item
from app.forms import RegistrationForm
from werkzeug.security import check_password_hash
from urllib.parse import urlparse
import re

print(f"*** app object imported into routes.py: {app}")  

@app.route('/')
def index():
    print("*** Inside the index route!")  
    return redirect(url_for('home'))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if form.validate_on_submit():
        email = form.email.data

        # Validate DUT email
        if not re.match(r"^\d{8}@dut4life\.ac\.za$", email):
            flash('Invalid DUT email format. Use an 8-digit student number followed by @dut4life.ac.za (e.g., 22212345@dut4life.ac\.za)', 'danger')
            return redirect(url_for('register'))

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already exists. Please log in.', 'danger')
            return redirect(url_for('login'))

        # Create new user
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=email,
            campus=form.campus.data
        )
        new_user.set_password(form.password.data)  

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created!', 'success')
            login_user(new_user)
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred during registration. Please try again.", "danger")
            return redirect(url_for('register'))

    return render_template('register.html', title='Register', form=form)

@app.route("/home")
def home():
    #add the flash message
    if not current_user.is_anonymous:
        flash("Login successful!", "success") 

    search_term = request.args.get('search', '')
    campus_filter = request.args.get('campus', 'all')
    date_filter = request.args.get('date', 'all')
    category_filter = request.args.get('category', 'all')

    query = Item.query

    if search_term:
        query = query.filter(Item.name.ilike(f"%{search_term}%"))
    if campus_filter != 'all':
        query = query.filter_by(campus=campus_filter)
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

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Validate DUT email
        if not re.match(r"^\d{8}@dut4life\.ac\.za$", email):
            flash('Invalid DUT email format. Use an 8-digit student number followed by @dut4life.ac\.za (e.g., 22212345@dut4life.ac\.za)', 'danger')
            return redirect(url_for("login"))

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':  
                next_page = url_for('home')
            return redirect(next_page)
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out.", "info")
    return redirect(url_for("home"))