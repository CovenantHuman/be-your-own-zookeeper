"""Crud operations"""

from model import db, User, ChecklistItem, Event, Activity, connect_to_db
import uuid
from passlib.hash import pbkdf2_sha256

def create_user(email, password, name):
    user = User(user_id=uuid.uuid4(), email=email, password=pbkdf2_sha256.hash(password), name=name)
    return user


if __name__ == "__main__":
    from server import app
    connect_to_db(app)