# app/__init__.py (With Admin & MyClaims, WITHOUT Mail)
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
# Removed: from flask_mail import Mail
from config import Config
import os

app = Flask(__name__, template_folder='../templates')
app.config.from_object(Config)

# Initialize Extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login' # Assuming 'login' is the correct endpoint name
login_manager.login_message_category = 'info'
# Removed: mail = Mail(app)

# Import models here to avoid circular imports
from app.models.user import User
from app.models.item import Item
# Removed: Claim model import (keep imports local to blueprints where needed)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Blueprint Registration with URL Prefixes ---
# Assuming blueprint objects are defined elsewhere (e.g., in __init__.py of feature)
from app.features.registration import registration_bp
from app.features.login import login_bp
from app.features.home import home_bp
from app.features.reports import reports_bp
from app.features.my_listings import my_listings_bp
from app.features.claims import claims_bp
from app.features.admin import admin_bp # Include admin blueprint import
from app.features.my_claims import my_claims_bp # Include my_claims blueprint import

app.register_blueprint(registration_bp, url_prefix='/register')
app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(home_bp, url_prefix='/')
app.register_blueprint(reports_bp, url_prefix='/report')
app.register_blueprint(my_listings_bp, url_prefix='/my_listings')
app.register_blueprint(claims_bp, url_prefix='/claims')
app.register_blueprint(admin_bp, url_prefix='/admin') # Include admin registration
app.register_blueprint(my_claims_bp, url_prefix='/my-claims') # Include my_claims registration

# --- End Blueprint Registration ---

# --- Upload Folder & DB Creation Setup ---
with app.app_context():
    # db.create_all() # Keep commented if using migrations
    # Corrected Upload Path Logic
    upload_folder_config = os.path.normpath(app.config.get('UPLOAD_FOLDER', 'app/static/uploads'))
    if 'app/' in upload_folder_config:
         upload_path = os.path.join(app.root_path, upload_folder_config.split('app/', 1)[-1])
    else:
         upload_path = os.path.join(app.instance_path, upload_folder_config)

    print(f"Checking/Creating Upload Path: {upload_path}")
    if not os.path.exists(upload_path):
        try:
            os.makedirs(upload_path)
            print(f"Created directory: {upload_path}")
        except OSError as e:
            print(f"Error creating directory {upload_path}: {e}")

    # Conditional DB creation
    if os.getenv('FLASK_ENV') == 'development':
        print("Development environment detected. Running db.create_all()...")
        db.create_all()
        print("db.create_all() finished.")
    else:
        print("Production or non-development environment detected. Skipping db.create_all(). Use Flask-Migrate.")
# --- End Setup Logic ---