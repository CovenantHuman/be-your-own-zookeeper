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
    checklist = create_default_checklist(user)
    return user, checklist

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

def update_user_account_preferences(user, name, email, zipcode, phone):
    """Update user account preferences"""
    user.name = name
    user.email = email
    user.zipcode = zipcode
    user.phone = phone

def update_user_password(user, password):
    """Update user password"""
    user.password=pbkdf2_sha256.hash(password)
    
def create_checklist_item(user, category, question, advice, order):
    """Create a new checklist_item."""
    checklist_item = ChecklistItem(item_id=uuid.uuid4(), 
                                    user_id = user.user_id,
                                    category=category, 
                                    question=question,
                                    advice=advice,
                                    order=order)
    return checklist_item

def create_default_checklist(user):
    """Create the default checklist items for a new user."""
    new_checklist = []
    new_checklist.append(create_checklist_item(user, 
                                                "Hydration", 
                                                "Have you had water recently?", 
                                                "Try drinking a small glass of water. \
                                                If you realize you're thirsty, go ahead and have more.",
                                                1))
    new_checklist.append(create_checklist_item(user,
                                                "Hunger",
                                                "Have you eaten recently?",
                                                "Try having a small snack. \
                                                If you realize you're hungry, go ahead and have more.",
                                                2))
    new_checklist.append(create_checklist_item(user,
                                                "Movement",
                                                "Have you moved your body recently?",
                                                "Try going for a walk or doing an alternate activity.",
                                                3))
    new_checklist.append(create_checklist_item(user,
                                                "Rest",
                                                "Have you gotten enough sleep recently?",
                                                "Try lying down for a little while. \
                                                If you realize you're tired, go ahead and have a longer rest.",
                                                4))
    new_checklist.append(create_checklist_item(user,
                                                "Pharmaceuticals",
                                                "Have you taken all the medications you're supposed to take?",
                                                "If you can, take them now.",
                                                5))
    new_checklist.append(create_checklist_item(user,
                                                "Social",
                                                "Have you talked to someone you love recently?",
                                                "Try texting someone you love.",
                                                6))
    new_checklist.append(create_checklist_item(user,
                                                "Hygiene",
                                                "Have you bathed recently?",
                                                "Try taking a bath or a shower. \
                                                If you don't have time, try washing your hands and face.",
                                                7))
    return new_checklist

if __name__ == "__main__":
    from server import app
    connect_to_db(app)