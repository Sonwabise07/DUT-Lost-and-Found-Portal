#app/features/registration/__init__.py
from flask import Blueprint

registration_bp = Blueprint('registration', __name__, template_folder='templates')

from app.features.registration.routes import register