"""Crud operations"""

from model import db, User, ChecklistItem, Event, Activity, connect_to_db
import uuid
from passlib.hash import pbkdf2_sha256
import random

def create_user(email, password, name, zipcode):
    """Create a new user."""
    user = User(user_id=uuid.uuid4(), 
                email=email, 
                password=pbkdf2_sha256.hash(password), 
                name=name, 
                zipcode=zipcode)
    checklist = create_default_checklist(user)
    activities = create_default_activities(user)
    return [user, checklist, activities]

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
    
def create_checklist_item(user, question, advice, order):
    """Create a new checklist_item."""
    for checklist_item in user.checklist_items:
        if checklist_item.order >= order:
            checklist_item.order += 1
    checklist_item = ChecklistItem(item_id=uuid.uuid4(), 
                                    user_id = user.user_id,
                                    question=question,
                                    advice=advice,
                                    order=order)
    return checklist_item

def create_default_checklist(user):
    """Create the default checklist items for a new user."""
    new_checklist = []
    new_checklist.append(create_checklist_item(user, 
                                                "Have you had water recently?", 
                                                "Try drinking a small glass of water. If you realize you're thirsty, go ahead and have more.",
                                                1))
    new_checklist.append(create_checklist_item(user,
                                                "Have you eaten recently?",
                                                "Try having a small snack. If you realize you're hungry, go ahead and have more.",
                                                2))
    new_checklist.append(create_checklist_item(user,
                                                "Have you moved your body recently?",
                                                "Try going for a walk or doing an alternate activity.",
                                                3))
    new_checklist.append(create_checklist_item(user,
                                                "Have you gotten enough sleep recently?",
                                                "Try lying down for a little while. If you realize you're tired, go ahead and have a longer rest.",
                                                4))
    new_checklist.append(create_checklist_item(user,
                                                "Have you taken all the medications you're supposed to take?",
                                                "If you can, take them now.",
                                                5))
    new_checklist.append(create_checklist_item(user,
                                                "Have you talked to someone you love recently?",
                                                "Try texting someone you love.",
                                                6))
    new_checklist.append(create_checklist_item(user,
                                                "Have you bathed recently?",
                                                "Try taking a bath or a shower. If you don't have time, try washing your hands and face.",
                                                7))
    return new_checklist

def get_checklist_item_by_id(id):
    """Get checklist item by its id"""
    return ChecklistItem.query.filter(ChecklistItem.item_id == id).first()

def get_user_checklist_in_order(user):
    """Get user checklist in order by order"""
    return ChecklistItem.query.filter(ChecklistItem.user_id == user.user_id).order_by(ChecklistItem.order)

def edit_checklist_item(user, item, question, advice, order):
    """Edit an individual checklist item"""
    item.question = question
    item.advice = advice
    prev_order = item.order
    if prev_order > order:
        for checklist_item in user.checklist_items:
            if checklist_item.order >= order and checklist_item.order < prev_order:
                checklist_item.order += 1
    elif prev_order < order:
        for checklist_item in user.checklist_items:
            if checklist_item.order <= order and checklist_item.order > prev_order:
                checklist_item.order -= 1
    item.order = order

    

def delete_checklist_item(user, item):
    """Delete an individual checklist item"""
    order = item.order
    for instance in user.checklist_items:
        if instance.order > order:
            instance.order -= 1
    db.session.delete(item)
   

def create_activity(user, name):
    """Create a new activity."""
    activity = Activity(activity_id=uuid.uuid4(), 
                        user_id = user.user_id,
                        name=name)
    return activity

def create_default_activities(user):
    """Create a list of default activities."""
    activities = []
    activities.append(create_activity(user, "Yoga"))
    activities.append(create_activity(user, "Jumping jacks"))
    activities.append(create_activity(user, "Sit ups"))
    activities.append(create_activity(user, "Private dance party"))
    activities.append(create_activity(user, "Push ups"))
    return activities

def get_activity_by_id(id):
    """Get activity for a given id"""
    return Activity.query.filter(Activity.activity_id == id).first()

def get_random_activity(user):
    """Get a random activity from a users alternate activities list"""
    activities = user.activities
    return random.choice(activities)

def remove_activity(activity):
    """Remove activity"""
    db.session.delete(activity)
    
def create_event(user, event_type, time, description, reminder):
    """Create a new event"""
    event = Event(event_id=uuid.uuid4(),
                user_id=user.user_id,
                event_type=event_type,
                time=time,
                description=description,
                reminder=reminder)
    return event

def edit_event(event, event_type, time, description, reminder):
    """Edit an existing event"""
    event.event_type = event_type
    event.time = time
    event.description = description
    event.reminder = reminder

def get_events_by_time(time):
    """Get events by time"""
    return Event.query.filter(Event.time == time).all()

def get_event_by_id(id):
    """Get event for a given id"""
    return Event.query.filter(Event.event_id == id).first()

def remove_event(event):
    """Remove event"""
    db.session.delete(event)


if __name__ == "__main__":
    from server import app
    connect_to_db(app)