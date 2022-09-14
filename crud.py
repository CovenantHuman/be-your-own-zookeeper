"""Crud operations"""

from model import db, User, ChecklistItem, Event, Activity, connect_to_db
import uuid
from passlib.hash import pbkdf2_sha256

def create_user(email, password, name):
    """Create a new user."""
    user = User(user_id=uuid.uuid4(), email=email, password=pbkdf2_sha256.hash(password), name=name)
    return user

def get_user_by_email(email):
    """Find a user by their email."""
    return User.query.filter(User.email == email).first()

if __name__ == "__main__":
    from server import app
    connect_to_db(app)