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
                zipcode=zipcode)
    return user

def get_user_by_email(email):
    """Find a user by their email."""
    return User.query.filter(User.email == email).first()

def update_user_weather_preferences(user, 
                                    temp_unit, 
                                    max_temp, 
                                    min_temp, 
                                    max_hum, 
                                    wind_unit, 
                                    max_wind_speed, 
                                    max_clouds, 
                                    min_clouds,
                                    rain, 
                                    snow,
                                    day,
                                    night):
    """Update user weather preferences"""
    user.is_fahrenheit = temp_unit
    user.max_temp = max_temp
    user.min_temp = min_temp
    user.max_hum = max_hum
    user.is_imperial = wind_unit
    user.max_wind_speed = max_wind_speed
    user.max_clouds = max_clouds
    user.min_clouds = min_clouds
    user.rain = rain
    user.snow = snow
    user.daylight = day
    user.night = night

if __name__ == "__main__":
    from server import app
    connect_to_db(app)