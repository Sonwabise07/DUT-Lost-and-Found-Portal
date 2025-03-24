from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.item import Item  # Import Item model
from .forms import EditItemForm #Import forms

my_listings_bp = Blueprint('my_listings', __name__, template_folder='templates')

@my_listings_bp.route('/my_listings')
@login_required
def my_listings():
    items = Item.query.filter_by(reporter=current_user).all()
    return render_template('my_listings/my_listings.html', items=items)

@my_listings_bp.route('/mark_returned/<int:item_id>', methods=['POST'])
@login_required
def mark_returned(item_id):
    item = Item.query.get_or_404(item_id)

    # Authorization check: Only the reporter can mark as returned
    if current_user.id != item.reporter.id:
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('home.home'))

    # Check if there's an approved claim
    claim = item.claims[0] if item.claims else None
    if not claim or claim.claim_status != 'approved':
        flash('This item cannot be marked as returned yet.', 'warning')
        return redirect(url_for('my_listings.my_listings'))

    item.returned = True
    db.session.commit()
    flash('Item marked as returned.', 'success')
    return redirect(url_for('my_listings.my_listings'))

@my_listings_bp.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)

    # Authorization check: Only the reporter can edit
    if current_user.id != item.reporter.id:
        flash('You are not authorized to edit this item.', 'danger')
        return redirect(url_for('my_listings.my_listings'))

     # Check if the item has been claimed or returned
    if item.claims or item.returned:
        flash('You cannot edit an item that has been claimed or returned.', 'warning')
        return redirect(url_for('my_listings.my_listings'))

    form = EditItemForm(obj=item)  # Pre-populate the form with item data

    if form.validate_on_submit():
        item.title = form.title.data
        item.description = form.description.data
        item.category = form.category.data
        item.campus= form.campus.data
        item.location_found = form.location_found.data
        # item.image_filename = form.image_filename.data # We will handle images later
        db.session.commit()
        flash('Item updated successfully!', 'success')
        return redirect(url_for('my_listings.my_listings'))

    return render_template('my_listings/edit_item.html', form=form, item=item)

@my_listings_bp.route('/delete_item/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)

    # Authorization check: Only the reporter can delete
    if current_user.id != item.reporter.id:
        flash('You are not authorized to delete this item.', 'danger')
        return redirect(url_for('my_listings.my_listings'))

    # Check if the item has been claimed or returned
    if item.claims or item.returned:
        flash('You cannot delete an item that has been claimed or returned.', 'warning')
        return redirect(url_for('my_listings.my_listings'))

    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('my_listings.my_listings'))