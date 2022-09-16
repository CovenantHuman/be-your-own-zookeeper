"""Crud operations"""

from model import db, User, ChecklistItem, Event, Activity, connect_to_db
import uuid
from passlib.hash import pbkdf2_sha256

def create_user(email, password, name, zipcode):
    """Create a new user."""
    user = User(user_id=uuid.uuid4(), 
                email=email, 
                password=pbkdf2_sha256.hash(password), 
                name=name, 
                zipcode=zipcode,
                max_temp=80,
                min_temp=60,
                is_fahrenheit=True,
                max_hum=100,
                max_wind_speed=18,
                is_imperial=True,
                max_clouds=100,
                min_clouds=0,
                rain=False,
                snow=False,
                daylight=True,
                night=False)
    return user

def get_user_by_email(email):
    """Find a user by their email."""
    return User.query.filter(User.email == email).first()

if __name__ == "__main__":
    from server import app
    connect_to_db(app)