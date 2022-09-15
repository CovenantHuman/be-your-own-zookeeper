"""Server for self care app."""

from flask import(Flask, render_template, request, flash, session, redirect, jsonify)
from jinja2 import StrictUndefined
import requests
import os
import crud
from model import connect_to_db, db
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
OPEN_WEATHER_KEY = os.environ["OPEN_WEATHER_KEY"]

@app.route("/")
def show_homepage():
    """Show homepage"""
    return render_template("homepage.html")

@app.route("/new-account")
def show_create_account_page():
    """Show the create an account page."""
    return render_template("create_account.html")

@app.route("/create-account", methods=["POST"])
def process_create_account():
    """Create a new user account"""
    name = request.form.get("name")
    zipcode = request.form.get("zipcode")
    email = request.form.get("email")
    password = request.form.get("password")
    if crud.get_user_by_email(email):
        flash("An account with this email already exists. Please login.")
        return redirect("/")
    else:
        user = crud.create_user(email, password, name, zipcode)
        db.session.add(user)
        db.session.commit()
        flash("Thanks for creating an account! Please login.")
        return redirect("/")

@app.route("/login")
def show_login_page():
    """Show the login page"""
    return render_template("login.html")

@app.route("/login-user", methods=["POST"])
def process_login():
    """Log in user if password is correct."""
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    if pbkdf2_sha256.verify(password, user.password):
        session['user_email'] = user.email
        flash('Logged in!')
    else:
        flash('Not logged in!')
    return redirect("/")

@app.route("/logout")
def process_logout():
    """Log out user"""
    del session['user_email']
    flash("You have been logged out!")
    return redirect("/")

@app.route("/zip-form")
def process_get_weather():
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

    