# app/features/login/__init__.py (CORRECTED)
from flask import Blueprint

# Define the blueprint HERE
login_bp = Blueprint('login', __name__, template_folder='templates')

# Import the routes module AFTER defining the blueprint
from . import routes