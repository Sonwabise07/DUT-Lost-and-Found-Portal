from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db, app  # Import 'app' here!
from app.features.reports.forms import ReportForm
from app.models.item import Item
from werkzeug.utils import secure_filename
import os
from PIL import Image
import uuid
from datetime import datetime

reports_bp = Blueprint('reports', __name__, template_folder='templates')

@reports_bp.route('/report/new', methods=['GET', 'POST'])
@login_required
def new_report():
    form = ReportForm()
    if request.method == 'POST':
        print("*** Form submitted!")
        if form.validate_on_submit():
            print("*** Form validated!")

            # --- Actual Submission Logic ---
            # Extract data from the form (using .data to get the values)
            title = form.title.data
            description = form.description.data
            category = form.category.data
            if category == 'Other':
                category = form.other_category.data  # Use "Other" category if selected
            campus = form.campus.data

            if campus == "Other":
                location_found = form.other_location.data
            else:
                location_found = form.location_found.data


            date_found = form.date_found.data  # It's ALREADY a date object
            # time_found = form.time_found.data  #It is already a time object REMOVED


            # ---  IMAGE HANDLING (START) ---
            image = request.files.get('image')
            filename = None

            if image:  # Check if an image was actually uploaded
                if allowed_file(image.filename):
                    # Generate a unique filename
                    filename = secure_filename(image.filename)
                    filename = f"{uuid.uuid4()}_{filename}"  # Add a UUID for uniqueness
                    # Use os.path.join *and* app.root_path
                    filepath = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
                    print(f"*** Filepath: {filepath}")

                    try:
                        # Save the original image
                        image.save(filepath)
                        print("*** Image saved successfully (original)")

                        # --- Image Resizing ---
                        img = Image.open(filepath)
                        print("*** Image opened with Pillow")
                        img.thumbnail((500, 500))
                        print("*** Thumbnail created (500x500)")
                        img.save(filepath)  # Overwrite original
                        print("*** Image resized and saved (500x500)")

                        thumb_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], "thumb_" + filename) #Also use root_path here
                        img.thumbnail((100, 100))
                        img.save(thumb_path)
                        print("*** Thumbnail saved (100x100)")

                    except Exception as e:
                        # Handle image processing errors (e.g., invalid image format)
                        print(f"*** Image processing error: {e}")  # DETAILED ERROR
                        flash('Could not process image. Please ensure it is a valid image file and not corrupted.', 'error')
                        if os.path.exists(filepath):  # Delete the file if it was saved
                            os.remove(filepath)
                        return render_template('reports/report_item.html', form=form)

                else:
                    flash('Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.', 'error')
                    return render_template('reports/report_item.html', form=form)
            # --- IMAGE HANDLING (END) ---

            # --- Contact Details ---
            contact_method = form.contact_method.data
            phone_number = form.phone_number.data
            whatsapp_number = form.whatsapp_number.data
            social_media_handle = form.social_media_handle.data
            email_addrs = form.email.data

            # --- Create and save the ReportItem ---
            report = Item(
                title=title,
                description=description,
                category=category,
                campus= campus,
                location_found=location_found,
                date_found=date_found,
                # time_found=time_found,  Removed
                image_filename=filename,
                user_id=current_user.id,
                contact_method = contact_method,
                phone_number = phone_number,
                whatsapp_number = whatsapp_number,
                social_media = social_media_handle,
                email = email_addrs
            )
            db.session.add(report)
            db.session.commit()


            flash('Report submitted successfully!', 'success')
            return redirect(url_for('home.home'))#changed
        else:
            print("*** Form did NOT validate!")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"    Error in field {field}: {error}")  # Corrected f-string

    return render_template('reports/report_item.html', form=form)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']