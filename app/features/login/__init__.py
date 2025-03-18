#app/features/login/__init__.py
from flask import Blueprint

login_bp = Blueprint('login', __name__, template_folder='templates')

from app.features.login.routes import login, logout