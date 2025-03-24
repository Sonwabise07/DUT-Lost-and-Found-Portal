from app import create_app  # Import create_app FUNCTION

app = create_app()  # Call the function to create an instance of Flask app

if __name__ == "__main__":
    app.run(debug=True)  # Run Flask app
