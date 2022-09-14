"""Server for self care app."""

from flask import(Flask, render_template, request, flash, session, redirect, jsonify)
from jinja2 import StrictUndefined
import requests
import os
import crud
from model import connect_to_db, db

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
OPEN_WEATHER_KEY = os.environ["OPEN_WEATHER_KEY"]

@app.route("/")
def homepage():
    """Show homepage"""
    return render_template("homepage.html")

@app.route("/new-account")
def new_account():
    """Show the create an account page."""
    return render_template("create_account.html")

@app.route("/create-account", methods=["POST"])
def create_account():
    """Creates a new user account."""
    # TODO: Once I have users in the database add a test here to make sure that 
    # email is not already in use before creating new account.
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.create_user(email, password, name)
    db.session.add(user)
    db.session.commit()
    flash("Thanks for creating an account! Please login.")
    return redirect("/")

@app.route("/zip-form")
def get_weather():
    """Take in the zipcode and gets the weather"""
    zipcode = request.args.get("zipcode")
    zip_with_country_code = zipcode + ",us"
    url = "https://api.openweathermap.org/data/2.5/weather"
    payload = {"zip": zip_with_country_code, "appid": OPEN_WEATHER_KEY}
    response = requests.get(url, params=payload)
    data = response.json()
    return jsonify(data)



if __name__ == "__main__":
    connect_to_db(app)
    
    app.run(host="0.0.0.0", debug=True)

    