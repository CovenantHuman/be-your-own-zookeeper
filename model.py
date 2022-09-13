"""Models for Be Your Own Zookeeper"""

from time import daylight
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
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

    def __repr__ (self):
        return f"<User user_id={self.user_id} email={self.email}>"

class ChecklistItems(db.Model):
    """An item on the checklist."""

    __tablename__= "checklist_items"

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    category = db.Column(db.String)
    question = db.Column(db.String)
    advice = db.Column(db.String)

    def __repr__(self):
        return f"<ChecklistItem item_id={self.item_id} question={self.question}>"


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