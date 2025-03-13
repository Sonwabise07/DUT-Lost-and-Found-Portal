from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

# Configuration settings
app.config['SECRET_KEY'] = 'your-secret-key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Change the URI if using another DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"  

from app import routes, models 

