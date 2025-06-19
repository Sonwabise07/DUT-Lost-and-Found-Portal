# app/features/my_claims/routes.py
from flask import render_template
from flask_login import login_required, current_user
# Import the blueprint object DEFINED in __init__.py
from . import my_claims_bp
from app.features.claims.models import Claim # Assuming Claim model is here

@my_claims_bp.route('/') # Use the imported blueprint object
@login_required
def list_user_claims():
    """Displays a list of claims submitted by the current user."""
    user_claims = Claim.query.filter_by(user_id=current_user.id)\
                             .order_by(Claim.agreement_timestamp.desc())\
                             .all()

    # Ensure template path includes the subfolder
    return render_template('my_claims_list.html', claims=user_claims)