from flask import Blueprint

my_listings_bp = Blueprint('my_listings', __name__, template_folder='templates')

from . import routes