# app/utils.py
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # --- CRITICAL CHECK ---
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('home.home'))  # Redirect non-admins
        # --- END CRITICAL CHECK ---
        return f(*args, **kwargs)
    return decorated_function