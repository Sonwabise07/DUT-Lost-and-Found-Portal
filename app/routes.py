from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User, Item
from app.forms import RegistrationForm
from werkzeug.security import check_password_hash
import re  # Import the regular expression module


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("home"))

    if form.validate_on_submit():
        email = form.email.data
        # Corrected regex: More robust DUT email validation
        if not re.match(r"^\d{8}@dut4life\.ac\.za$", email):
            #   Enhanced error message for register
            flash(
                'Invalid DUT email format. Please use an 8-digit student number followed by @dut4life.ac.za (e.g., 22212345@dut4life.ac.za)',
                'danger')
            return render_template('register.html', title='Register', form=form)

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists. Please log in.', 'danger')
            return redirect(url_for('login'))

        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=email,
            campus=form.campus.data
        )
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created!', 'success')

        login_user(new_user)
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route("/home")
def home():
    search_term = request.args.get('search', '')
    campus_filter = request.args.get('campus', 'all')
    date_filter = request.args.get('date', 'all')
    category_filter = request.args.get('category', 'all')

    items = Item.query.all()

    if search_term:
        items = [item for item in items if search_term.lower() in item.name.lower()]

    if campus_filter != 'all':
        items = [item for item in items if item.campus == campus_filter]

    # ... (Implement date filtering logic here if needed) ...

    if category_filter != 'all':
        items = [item for item in items if item.category == category_filter]

    recent_listings = items[-10:]

    return render_template('home.html',
                           recent_listings=recent_listings,
                           search_term=search_term,
                           campus_filter=campus_filter,
                           date_filter=date_filter,
                           category_filter=category_filter)


@app.route("/report_item", methods=["GET", "POST"])
@login_required
def report_item():
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        location = request.form.get('location')
        campus = request.form.get('campus')
        category = request.form.get('category')

        new_item = Item(
            name=name,
            description=description,
            location=location,
            campus=campus,
            category=category,
            # ... (Set other item attributes)
        )

        db.session.add(new_item)
        db.session.commit()

        flash("Item reported successfully!", "success")
        return redirect(url_for('home'))

    return render_template('report_item.html')  # Create a template for this form


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Corrected regex: More robust DUT email validation
        if not re.match(r"^\d{8}@dut4life\.ac\.za$", email):
            #   Enhanced error message for login
            flash(
                'Invalid DUT email format. Please use an 8-digit student number followed by @dut4life.ac.za (e.g., 22212345@dut4life.ac.za)',
                'danger')
            return render_template("login.html")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password.", "danger")
            return render_template("login.html")
    return render_template("login.html")  # This line handles GET requests


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))