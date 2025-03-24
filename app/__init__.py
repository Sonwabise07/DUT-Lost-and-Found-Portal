from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config
import os

# Initialize extensions (without attaching to app yet)
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login.login'  # Use blueprint.function_name
login_manager.login_message_category = 'info' # Add this line for flash message styling

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(Config)

    # Initialize extensions WITH app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Import models here to avoid circular imports
    from app.models.user import User
    from app.models.item import Item

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # --- Blueprint Registration with URL Prefixes ---
    from app.features.registration.routes import registration_bp
    from app.features.login.routes import login_bp
    from app.features.home.routes import home_bp
    from app.features.reports.routes import reports_bp
    from app.features.my_listings.routes import my_listings_bp
    from app.features.claims.routes import claims_bp

    app.register_blueprint(registration_bp, url_prefix='/register')  # Added url_prefix
    app.register_blueprint(login_bp, url_prefix='/login')          # Added url_prefix
    app.register_blueprint(home_bp, url_prefix='/')              # Added url_prefix (root)
    app.register_blueprint(reports_bp, url_prefix='/report')       # Added url_prefix
    app.register_blueprint(my_listings_bp, url_prefix='/my_listings') # Added url_prefix
    app.register_blueprint(claims_bp, url_prefix='/claims')         # Added url_prefix

    # --- End Blueprint Registration ---

    with app.app_context():
        db.create_all()  # Create tables if they don't exist
        # Ensure UPLOAD_FOLDER exists
        upload_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

    return app  # Return the app instance