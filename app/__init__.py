from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import os

app = Flask(__name__, template_folder='../templates')  # Template folder is OUTSIDE app
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'  # Use blueprint.function_name

# Import models here to avoid circular imports
from app.models.user import User
from app.models.item import Item

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Blueprint Registration ---
from app.features.registration.routes import registration_bp
from app.features.login.routes import login_bp
from app.features.home.routes import home_bp
from app.features.reports.routes import reports_bp
from app.features.my_listings.routes import my_listings_bp  # Import the new blueprint


app.register_blueprint(registration_bp)
app.register_blueprint(login_bp)
app.register_blueprint(home_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(my_listings_bp)  # Register the new blueprint
# --- End Blueprint Registration ---

with app.app_context():
    db.create_all()