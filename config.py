import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-dev-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Use PostgreSQL on Render (DATABASE_URL set by Render automatically)
    # Fall back to SQLite locally
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')

    # Render gives a URL starting with "postgres://" but SQLAlchemy needs "postgresql://"
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = database_url