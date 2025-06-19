from flask import Blueprint

my_claims_bp = Blueprint('my_claims', __name__, template_folder='templates')

# Routes MUST be imported AFTER the blueprint is defined
from . import routes