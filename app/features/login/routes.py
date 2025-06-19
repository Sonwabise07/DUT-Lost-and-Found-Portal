# app/features/login/routes.py (CORRECTED)
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db, bcrypt # Import db and bcrypt from main app
from app.models.user import User
from werkzeug.security import check_password_hash # Keep if using directly, else remove
from urllib.parse import urlparse, urljoin
import re
# Import the blueprint object DEFINED IN __init__.py
from . import login_bp
# Import the form if you decide to use WTForms later
# from .forms import LoginForm

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.home"))

    if request.method == "POST":
        email = request.form.get("email") # Use .get() for safety
        password = request.form.get("password")

        if not email or not password:
             flash("Email and password are required.", "danger")
             return render_template("login.html") # Re-render on missing data

        # Validate DUT email
        if not re.match(r"^\d{8}@dut4life\.ac\.za$", email):
            flash('Invalid DUT email format. Use an 8-digit student number followed by @dut4life.ac.za', 'danger')
            return render_template("login.html") # Re-render on format error

        user = User.query.filter_by(email=email).first()

        # Use bcrypt for checking hash
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            # Basic safety check for next_page URL
            if not next_page or urlparse(next_page).netloc != '':
                if user.role == 'admin':
                    next_page = url_for('admin.admin_dashboard') # Correct endpoint
                else:
                    next_page = url_for('home.home')
            flash("Login successful!", "success")
            return redirect(next_page)
        else:
            flash("Invalid email or password.", "danger")
            return render_template("login.html") # Re-render on auth failure

    # GET request
    return render_template("login.html") # Template path corrected

@login_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out.", "info")
    return redirect(url_for("home.home"))