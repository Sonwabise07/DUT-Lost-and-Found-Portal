# run.py
from app import app, db  # Import the 'app' object directly
from app.models.user import User  # Import User
import click

@app.cli.command("create-admin")
@click.argument("email")
@click.argument("password")
@click.argument("first_name")
@click.argument("last_name")
@click.argument("campus")
def create_admin(email, password, first_name, last_name, campus):
    """Creates an admin user."""
    with app.app_context():
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"Error: User with email '{email}' already exists.")
            return

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            campus=campus,
            role='admin'
        )
        user.set_password(password)  # Corrected: Use set_password
        db.session.add(user)
        db.session.commit()
        print(f"Admin user '{email}' created successfully.")

if __name__ == '__main__':
    app.run(debug=True)