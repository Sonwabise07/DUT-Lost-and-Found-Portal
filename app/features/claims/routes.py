from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.item import Item
from app.features.claims.models import Claim  # Import the Claim model
from datetime import datetime

claims_bp = Blueprint('claims', __name__, template_folder='templates')

def update_claim_status(claim_id, status):
    """Helper function to update claim status."""
    claim = Claim.query.get_or_404(claim_id)
    claim.claim_status = status
    db.session.commit()

@claims_bp.route('/claim/<int:item_id>', methods=['GET', 'POST'])  # Handle GET and POST
@login_required
def claim_item(item_id):
    item = Item.query.get_or_404(item_id)

    # Authorization checks (Keep these)
    if current_user.id == item.reporter.id:
        flash('You cannot claim an item you reported.', 'warning')
        return redirect(url_for('home.item_detail', item_id=item.id))

    # Check if the item has already been claimed
    existing_claim = Claim.query.filter_by(item_id=item.id).first()
    if existing_claim:
        flash('This item has already been claimed.', 'warning')
        return redirect(url_for('home.item_detail', item_id=item.id))


    if request.method == 'POST':
        # Handle the form submission (POST request)
        typed_name = request.form.get('typed_name')  # Get the typed name from the form

        # Validate the typed name against the user's full name
        if typed_name != current_user.full_name:  # Use the full_name property!
            flash('The typed name does not match your registered full name.', 'danger')
            return render_template('claim_agreement.html', item=item)

        # Create the Claim object
        agreement_text = """
DURBAN UNIVERSITY OF TECHNOLOGY (DUT) LOST AND FOUND CLAIM AGREEMENT
This Agreement is a legally binding document between Durban University of Technology (DUT) and the claimant. By signing this document, you acknowledge that you are the rightful owner of the item you are claiming. Providing false information or attempting to fraudulently claim an item that does not belong to you will result in serious consequences.
1. I hereby confirm that the item I am claiming is my personal property, and I can provide proof of ownership if required.
2. I understand that providing false information or attempting to claim an item that is not mine constitutes fraud and will result in immediate disciplinary action, including EXPULSION from Durban University of Technology.
3. I acknowledge that DUT reserves the right to verify my claim and that the final decision lies with the university’s administration.
4. I understand that if found guilty of fraudulent claims, I may also face CRIMINAL CHARGES, which could result in a permanent criminal record.
5. I accept full responsibility for the accuracy of the information provided and agree to abide by DUT’s policies regarding lost and found items.
6. I acknowledge that any attempt to interfere with or manipulate the lost and found process will be reported to law enforcement authorities.
        """  # Use the correctly formatted text.
        agreement_text = agreement_text.replace("[User Name]", current_user.full_name)


        claim = Claim(
            user_id=current_user.id,
            item_id=item.id,
            agreement_text=agreement_text,
            agreement_timestamp=datetime.utcnow(),  # Use .now() for timezone-naive
            claim_status='pending'
        )
        db.session.add(claim)
        db.session.commit()

        flash('Your claim has been submitted and is pending review.', 'success')
        return redirect(url_for('home.item_detail', item_id=item.id))

    # If it's a GET request, display the agreement form
    return render_template('claim_agreement.html', item=item)

@claims_bp.route('/approve_claim/<int:claim_id>')
@login_required  # In a real admin interface, you'd use a different decorator, like @admin_required
def approve_claim(claim_id):
    #For demonstration, we allow the item owner to approve.
    claim = Claim.query.get_or_404(claim_id)
    if current_user.id != claim.item.reporter.id:
        flash('You are not authorized to approve claims.', 'danger')
        return redirect(url_for('home.home'))

    update_claim_status(claim_id, 'approved')
    flash('Claim approved.', 'success')
    return redirect(url_for('my_listings.my_listings'))


@claims_bp.route('/reject_claim/<int:claim_id>')
@login_required
def reject_claim(claim_id):
    # For demonstration, we allow the item owner to reject.
    claim = Claim.query.get_or_404(claim_id)
    if current_user.id != claim.item.reporter.id:
        flash('You are not authorized to reject claims.', 'danger')
        return redirect(url_for('home.home'))

    update_claim_status(claim_id, 'rejected')
    flash('Claim rejected.', 'success')
    return redirect(url_for('my_listings.my_listings'))