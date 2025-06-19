from app import create_app, db
from app.models.user import User

app = create_app()

def create_admin_user(email, password, first_name, last_name, campus):
    with app.app_context():
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"Error: User with email '{email}' already exists.")
            return

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            campus=campus,
            role='admin'  # Set as admin
        )
        new_user.set_password(password)  # Hash the password
        db.session.add(new_user)
        db.session.commit()
        print(f"Admin user '{email}' created successfully.")


if __name__ == "__main__":
    # Replace with your desired admin details
    email = "22203924@dut4life.ac.za"
    password = "Admin@11"
    first_name = "Philani"
    last_name = "Myeni"
    campus = "SteveBiko"

    create_admin_user(email, password, first_name, last_name, campus)