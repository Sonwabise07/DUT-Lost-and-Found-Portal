from flask import Blueprint

admin_bp = Blueprint('admin', __name__, template_folder='templates')

def register_admin_routes():
    from . import routes  
