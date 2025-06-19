# app/features/admin/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.item import Item
from app.features.claims.models import Claim # Make sure Claim model is imported
from . import admin_bp
from app.utils import admin_required # Import the decorator
from .forms import ClaimApprovalForm

@admin_bp.route('/admin/claims')
@login_required
@admin_required
def list_claims():
    claims = Claim.query.all()
    # Remove 'admin/' prefix if list_claims.html is directly in admin/templates/
    return render_template('list_claims.html', claims=claims)

@admin_bp.route('/admin/claims/<int:claim_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_claim(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    form = ClaimApprovalForm(obj=claim)

    if form.validate_on_submit():
        claim.claim_status = form.status.data
        db.session.commit()
        flash('Claim status updated.', 'success')
        return redirect(url_for('admin.list_claims'))

    # Remove 'admin/' prefix if edit_claim.html is directly in admin/templates/
    return render_template('edit_claim.html', form=form, claim=claim)

@admin_bp.route('/admin/claims/<int:claim_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_claim(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    if claim.claim_status == 'pending':
        claim.claim_status = 'approved'
        item = Item.query.get(claim.item_id)
        if item:
             item.returned = True # Mark item as returned/claimed
             # item.claimed_by = claim.user_id # You might not have this field
        db.session.commit()
        flash(f'Claim {claim_id} approved.', 'success')
    else:
        flash(f'Claim {claim_id} is not pending or already processed.', 'warning')
    return redirect(url_for('admin.list_claims'))

@admin_bp.route('/admin/claims/<int:claim_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_claim(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    if claim.claim_status == 'pending':
        claim.claim_status = 'rejected'
        db.session.commit()
        flash(f'Claim {claim_id} rejected.', 'success')
    else:
        flash(f'Claim {claim_id} is not pending or already processed.', 'warning')
    return redirect(url_for('admin.list_claims'))

@admin_bp.route('/dashboard') # Or just '/' if prefix is '/admin'
@login_required
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    total_items = Item.query.count()
    pending_claims = Claim.query.filter_by(claim_status='pending').count()
    items = Item.query.order_by(Item.date_reported.desc()).all()
    claims = Claim.query.order_by(Claim.agreement_timestamp.desc()).all()

    # Remove 'admin/' prefix if admin_dashboard.html is directly in admin/templates/
    return render_template('admin_dashboard.html',
                           total_users=total_users,
                           total_items=total_items,
                           pending_claims=pending_claims,
                           items=items,
                           claims=claims)