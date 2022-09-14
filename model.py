"""Models for Be Your Own Zookeeper"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    zipcode = db.Column(db.String)
    phone = db.Column(db.String)
    max_temp = db.Column(db.Integer)
    min_temp = db.Column(db.Integer)
    max_hum = db.Column(db.Integer)
    max_wind_speed = db.Column(db.Integer)
    max_clouds = db.Column(db.Integer)
    min_clouds = db.Column(db.Integer)
    rain = db.Column(db.Boolean)
    snow = db.Column(db.Boolean)
    daylight = db.Column(db.Boolean)
    night = db.Column(db.Boolean)

    checklist_items = db.relationship("ChecklistItem", back_populates="user")
    events = db.relationship("Event", back_populates="user")
    activities = db.relationship("Activity", back_populates="user")

    def __repr__ (self):
        return f"<User user_id={self.user_id} email={self.email}>"

class ChecklistItem(db.Model):
    """An item on the checklist."""

    __tablename__= "checklist_items"

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=False)
    category = db.Column(db.String)
    question = db.Column(db.String)
    advice = db.Column(db.String)

    user = db.relationship("User", back_populates="checklist_items")

    def __repr__(self):
        return f"<ChecklistItem item_id={self.item_id} question={self.question}>"

class Event(db.Model):
    """An event in a schedule."""

    __tablename__= "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=False)
    event_type = db.Column(db.String)
    time = db.Column(db.DateTime)
    description = db.Column(db.String)
    reminder = db.Column(db.Boolean)
    completed = db.Column(db.Boolean)

    user = db.relationship("User", back_populates="events")

    def __repr__(self):
        return f"<Event event_id={self.event_id} description={self.description}>"

class Activity(db.Model):
    """An alternate activity in place of walking."""

    __tablename__= "activities"

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=False)
    name = db.Column(db.String)
    description = db.Column(db.String)

    user = db.relationship("User", back_populates="activities")

    def __repr__(self):
        return f"<Activity activity_id={self.activity_id} name={self.name}>"

def connect_to_db(flask_app, db_uri="postgresql:///zookeeper", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")



if __name__ == "__main__":
    from server import app

    connect_to_db(app)