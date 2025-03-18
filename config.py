import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-long-and-random-secret-key'  # REPLACE THIS
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///lostfound.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'  # Add this line
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB - Add this line
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Add this line