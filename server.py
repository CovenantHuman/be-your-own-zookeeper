"""Server for self care app."""
from flask import(Flask, render_template, request, flash, session, redirect, jsonify)
from jinja2 import StrictUndefined
import requests
import os
import crud
from model import connect_to_db, db
from passlib.hash import pbkdf2_sha256
import json

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
        user, checklist, activities = crud.create_user(email, password, name, zipcode)
        db.session.add(user)
        db.session.add_all(checklist)
        db.session.add_all(activities)
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
    if user:
        if pbkdf2_sha256.verify(password, user.password):
            session['user_email'] = user.email
            flash('Logged in!')
            return redirect("/user-homepage")
        else:
            flash('Not logged in!')
            return redirect("/")
    else:
        flash('Not logged in!')
        return redirect("/")

@app.route("/user-homepage")
def show_user_homepage():
    """Show user logged in homepage"""
    user = crud.get_user_by_email(session["user_email"])
    return render_template("/user_homepage.html", name=user.name, zipcode=user.zipcode)

@app.route("/weather-preferences")
def show_weather_preferences():
    """Show weather preferences page"""
    user = crud.get_user_by_email(session["user_email"])
    return render_template("weather_preferences.html", 
                            temp_unit=user.is_fahrenheit, 
                            max_temp=user.max_temp, 
                            min_temp=user.min_temp,
                            max_hum=user.max_hum,
                            wind_unit=user.is_imperial,
                            max_wind_speed=user.max_wind_speed,
                            max_clouds=user.max_clouds,
                            min_clouds=user.min_clouds,
                            rain=user.rain,
                            snow=user.snow,
                            day=user.daylight,
                            night=user.night)

@app.route("/update-weather-preferences", methods=["POST"])
def set_weather_preferences():
    """Set weather preferences"""
    temp_unit = request.form.get("temp_unit")
    if temp_unit == "fahrenheit":
        temp_unit = True
    else:
        temp_unit = False
    max_temp = request.form.get("max_temp")
    min_temp = request.form.get("min_temp")
    max_hum = request.form.get("humidity")
    wind_unit = request.form.get("wind_unit")
    if wind_unit == "imperial":
        wind_unit = True
    else:
        wind_unit = False
    max_wind_speed = request.form.get("wind")
    max_clouds = request.form.get("max_clouds")
    min_clouds = request.form.get("min_clouds")
    rain = request.form.get("rain")
    if rain == "true":
        rain = True
    else:
        rain = False
    snow = request.form.get("snow")
    if snow == "true":
        snow = True
    else:
        snow = False
    time = request.form.get("time")
    if time == "both":
        day = True
        night = True
    elif time == "day":
        day = True
        night = False
    else:
        day = False
        night = True
    user = crud.get_user_by_email(session["user_email"])
    crud.update_user_weather_preferences(user, 
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
                                        night)
    db.session.commit()
    flash("Weathe settings updated!")
    return redirect("/user-homepage")

@app.route("/alternate-activities")
def show_alternate_activities():
    """Show alternate activities editing page"""
    user = crud.get_user_by_email(session['user_email'])
    names = []
    for activity in user.activities:
        names.append(activity.name)
    return render_template("alternate_activities.html", names=names)

@app.route("/remove-alt-act/<name>")
def remove_alternate_activity(name):
    """Remove alternate activity"""
    user = crud.get_user_by_email(session['user_email'])
    activity = crud.get_activity_by_name(user, name)
    crud.remove_activity(activity)
    db.session.commit()
    flash(f"{name} removed!")
    return redirect("/alternate-activities")

@app.route("/add-activity", methods=["POST"])
def add_alternate_activity():
    user = crud.get_user_by_email(session["user_email"])
    name = request.form.get("new_activity")
    new_activity = crud.create_activity(user, name)
    db.session.add(new_activity)
    db.session.commit()
    flash(f"{name} added!")
    return redirect("/alternate-activities")

@app.route("/schedule")
def show_schedule():
    user = crud.get_user_by_email(session['user_email'])
    return render_template("schedule.html", name=user.name)

@app.route("/checklist-start")
def show_checklist_landing_page():
    """Show checklist landing page"""
    user = crud.get_user_by_email(session['user_email'])
    return render_template("checklist_start.html", name=user.name)

@app.route("/checklist-item/<order>")
def show_checklist_item(order):
    """Show a checklist item"""
    user = crud.get_user_by_email(session['user_email'])
    checklist_list = list(user.checklist_items)
    checklist_item_count = len(checklist_list)
    if int(order) >= checklist_item_count:
        return render_template("checklist_end.html",
                                name=user.name,
                                total=checklist_item_count)
    else:
        for item in checklist_list:
            if item.order == int(order):
                return render_template("checklist.html", 
                                        name=user.name,
                                        question=item.question, 
                                        advice=item.advice,
                                        order=item.order,
                                        total=checklist_item_count) 

@app.route("/account-preferences")
def show_account_preferences():
    """Show account preferences page"""
    user = crud.get_user_by_email(session['user_email'])
    return render_template("account_preferences.html",
                            name=user.name,
                            email=user.email,
                            zipcode=user.zipcode,
                            phone=user.phone)

@app.route("/update-account-preferences", methods=["POST"])
def update_account_preferences():
    """Update user's account preferences"""
    user = crud.get_user_by_email(session["user_email"])
    email = request.form.get("email")
    name = request.form.get("name")
    zipcode = request.form.get("zipcode")
    phone = request.form.get("phone")
    crud.update_user_account_preferences(user, name, email, zipcode, phone)
    db.session.commit()
    flash("Account settings updated!")
    return redirect("/user-homepage")

@app.route("/update-password", methods=["POST"])
def update_password():
    """Update user password"""
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")
    user = crud.get_user_by_email(session["user_email"])
    if pbkdf2_sha256.verify(old_password, user.password):
        if new_password == confirm_password:
            crud.update_user_password(user, new_password)
            db.session.commit()
            flash("Password updated!")
            return redirect("/user-homepage")
        else:
            flash("New password must match confirm password.")
            return redirect("/account-preferences")
    else:
        flash("Password incorrect. Please try again.")
        return redirect("/account-preferences")

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

@app.route("/api/user")
def process_get_user():
    """Get user from session and jsonify them"""
    if "user_email" in session:
        user = crud.get_user_by_email(session["user_email"])
        activities = []
        for activity in user.activities:
            activities.append(activity.name)
        return jsonify({"max_temp": user.max_temp,
                        "min_temp": user.min_temp,
                        "is_fahrenheit": user.is_fahrenheit,
                        "max_hum": user.max_hum,
                        "max_wind_speed": user.max_wind_speed,
                        "is_imperial": user.is_imperial,
                        "max_clouds": user.max_clouds,
                        "min_clouds": user.min_clouds,
                        "rain": user.rain,
                        "snow": user.snow,
                        "daylight": user.daylight,
                        "night": user.night,
                        "activities": activities})
    else:
        return jsonify({"max_temp": 80,
                        "min_temp": 60,
                        "is_fahrenheit": True,
                        "max_hum": 100,
                        "max_wind_speed": 4,
                        "is_imperial": True,
                        "max_clouds": 100,
                        "min_clouds": 0,
                        "rain": False,
                        "snow": False,
                        "daylight": True,
                        "night": False,
                        "activities": ["Yoga", 
                                        "Jumping jacks",
                                        "Sit ups",
                                        "Private dance party",
                                        "Push ups"]})


if __name__ == "__main__":
    connect_to_db(app)
    
    app.run(host="0.0.0.0", debug=True)

    