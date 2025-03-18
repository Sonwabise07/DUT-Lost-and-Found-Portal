from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db  # Import db
from app.models.user import User
from werkzeug.security import check_password_hash
from urllib.parse import urlparse
import re

from flask import Blueprint

login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.home"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Validate DUT email
        if not re.match(r"^\d{8}@dut4life\.ac\.za$", email):
            flash('Invalid DUT email format. Use an 8-digit student number followed by @dut4life.ac.za (e.g., 22212345@dut4life.ac\.za)', 'danger')
            return redirect(url_for("login.login"))

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('home.home')
            flash("Login successful!", "success") # ADD flash message here
            return redirect(next_page)
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("login.login"))

    return render_template("login.html")

@login_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out.", "info")
    return redirect(url_for("home.home"))