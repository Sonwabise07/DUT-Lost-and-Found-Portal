from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user
from app import db  # Import db from the main app
from app.models.user import User  # Import User model
from app.features.registration.forms import RegistrationForm  # Import forms
from werkzeug.security import check_password_hash
import re

from flask import Blueprint #import

registration_bp = Blueprint('registration', __name__, template_folder='templates') #create registration blueprint


@registration_bp.route("/register", methods=["GET", "POST"]) #use blueprint
def register():
    form = RegistrationForm()

    if current_user.is_authenticated:
        return redirect(url_for("home.home")) #change to blueprint

    if form.validate_on_submit():
        email = form.email.data

        # Validate DUT email
        if not re.match(r"^\d{8}@dut4life\.ac\.za$", email):
            flash('Invalid DUT email format. Use an 8-digit student number followed by @dut4life.ac.za (e.g., 22212345@dut4life.ac\.za)', 'danger')
            return redirect(url_for('registration.register'))#changed

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already exists. Please log in.', 'danger')
            return redirect(url_for('login.login'))#changed

        # Create new user
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=email,
            campus=form.campus.data
        )
        new_user.set_password(form.password.data)  # Ensure set_password() hashes the password

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created!', 'success')
            login_user(new_user)
            return redirect(url_for('home.home'))#changed
        except Exception as e:
            db.session.rollback()
            flash("An error occurred during registration. Please try again.", "danger")
            return redirect(url_for('registration.register'))#changed

    return render_template('register.html', title='Register', form=form) #changed