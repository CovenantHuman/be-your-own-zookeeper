"""Server for self care app."""
from flask import(Flask, render_template, request, flash, session, redirect, jsonify)
from jinja2 import StrictUndefined
import os
import crud
from model import connect_to_db, db
from passlib.hash import pbkdf2_sha256
import datetime
import weather

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
OPEN_WEATHER_KEY = os.environ["OPEN_WEATHER_KEY"]
EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
NAME = os.environ["NAME"]

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
    if session.get("user_email"):
        user = crud.get_user_by_email(session["user_email"])
        return render_template("/user_homepage.html", name=user.name, zipcode=user.zipcode)
    else:
        return redirect("/")

@app.route("/weather-preferences")
def show_weather_preferences():
    """Show weather preferences page"""
    if session.get("user_email"):
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
    else:
        return redirect("/")

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
    flash("Weather settings updated!")
    return redirect("/user-homepage")

@app.route("/alternate-activities")
def show_alternate_activities():
    """Show alternate activities editing page"""
    if session.get("user_email"):
        user = crud.get_user_by_email(session['user_email'])
        names = []
        for activity in user.activities:
            name_tuple = (activity.name, activity.activity_id)
            names.append(name_tuple)
        return render_template("alternate_activities.html", names=names)
    else:
        return redirect("/")

@app.route("/remove-alt-act/<id>")
def remove_alternate_activity(id):
    """Remove alternate activity"""
    activity = crud.get_activity_by_id(id)
    crud.remove_activity(activity)
    db.session.commit()
    flash(f"{activity.name} removed!")
    return redirect("/alternate-activities")

@app.route("/add-activity", methods=["POST"])
def add_alternate_activity():
    """Add an alternate activity"""
    user = crud.get_user_by_email(session["user_email"])
    name = request.form.get("new_activity")
    new_activity = crud.create_activity(user, name)
    db.session.add(new_activity)
    db.session.commit()
    flash(f"{name} added!")
    return redirect("/alternate-activities")

@app.route("/schedule")
def show_schedule():
    """Show schedule page"""
    if session.get("user_email"):
        user = crud.get_user_by_email(session['user_email'])
        user_events = user.events
        sorted_events = sorted(user_events, key= lambda event: event.time)
        events = []
        for sorted_event in sorted_events:
            user_time = sorted_event.time.strftime("%I:%M %p")
            events.append({"time": user_time, "description": sorted_event.description, "id":sorted_event.event_id})
        return render_template("schedule.html", name=user.name, events=events)
    else:
        return redirect("/")

@app.route("/new-event")
def show_add_event_page():
    """Show add event page"""
    if session.get("user_email"):
        return render_template("add_event.html")
    else:
        return redirect("/")

@app.route("/add-event", methods=["POST"])
def add_event():
    """Add or update an event"""
    user = crud.get_user_by_email(session["user_email"])
    event_type = request.form.get("event_type")
    event_time = request.form.get("time")
    event_time = datetime.datetime.strptime(event_time, "%H:%M")
    description = request.form.get("description")
    reminder = request.form.get("reminder")
    if reminder is None:
        reminder = False
    else:
        reminder = True 
    event = crud.create_event(user, event_type, event_time, description, reminder)
    db.session.add(event)
    db.session.commit()
    flash(f"{description} added!")
    return redirect("/schedule")
    

@app.route("/event-edit/<id>")
def show_edit_event(id):
    """Display the edit event page"""
    if session.get("user_email"):
        event = crud.get_event_by_id(id)
        return render_template("edit_event.html", 
                                id=id, 
                                event_type=event.event_type, 
                                time=datetime.datetime.strftime(event.time, "%H:%M"), 
                                description=event.description, 
                                reminder=event.reminder)
    else:
        return redirect("/")

@app.route("/edit-event/<id>", methods=["POST"])
def edit_event(id):
    """Edit event"""
    event = crud.get_event_by_id(id)
    event_type = request.form.get("event_type")
    event_time = request.form.get("time")
    event_time = datetime.datetime.strptime(event_time, "%H:%M")
    description = request.form.get("description")
    reminder = request.form.get("reminder")
    if reminder is None:
        reminder = False
    else:
        reminder = True 
    crud.edit_event(event, event_type, event_time, description, reminder)
    db.session.commit()
    flash(f"{description} updated!")
    return redirect("/schedule")


@app.route("/remove-event/<id>")
def remove_event(id):
    """Remove event"""
    event = crud.get_event_by_id(id)
    crud.remove_event(event)
    db.session.commit()
    flash(f"{event.description} removed!")
    return redirect("/schedule")

@app.route("/checklist-start")
def show_checklist_landing_page():
    """Show checklist landing page"""
    if session.get("user_email"):
        user = crud.get_user_by_email(session['user_email'])
        return render_template("checklist_start.html", name=user.name)
    else:
        return redirect("/")

@app.route("/checklist-item/<order>")
def show_checklist_item(order):
    """Show a checklist item"""
    if session.get("user_email"):
        user = crud.get_user_by_email(session['user_email'])
        checklist_list = list(user.checklist_items)
        checklist_item_count = len(checklist_list)
        if int(order) >= checklist_item_count+1:
            return render_template("checklist_end.html",
                                    name=user.name,
                                    total=checklist_item_count+1)
        else:
            for item in checklist_list:
                if item.order == int(order):
                    return render_template("checklist.html", 
                                            name=user.name,
                                            question=item.question, 
                                            advice=item.advice,
                                            order=item.order,
                                            total=checklist_item_count+1) 
    else:
        return redirect("/")

@app.route("/edit-checklist")
def show_checklist_edit_page():
    """Show checklist editing page"""
    if session.get("user_email"):
        user = crud.get_user_by_email(session['user_email'])
        items = []
        for item in crud.get_user_checklist_in_order(user):
            item_info = [item.question, item.item_id, item.order]
            items.append(item_info)
        return render_template("checklist_edit.html", items=items)
    else:
        return redirect("/")

@app.route("/new-checklist-item")
def show_new_checklist_item_page():
    """Show page for adding a new item to the checklist."""
    if session.get("user_email"):
        user = crud.get_user_by_email(session['user_email'])
        items = user.checklist_items
        count = len(items) + 1 
        return render_template("add_checklist_item.html", count=count)
    else:
        return redirect("/")

@app.route("/add-checklist-item", methods=["POST"])
def add_checklist_item():
    """Add a new item to the checklist."""
    user = crud.get_user_by_email(session['user_email'])
    order = int(request.form.get("order"))
    question = request.form.get("question")
    advice = request.form.get("advice")
    checklist_item = crud.create_checklist_item(user, question, advice, order)
    db.session.add(checklist_item)
    db.session.commit()
    flash(f"Added: {question}")
    return redirect("/edit-checklist")

@app.route("/edit-individual-checklist-item/<id>")
def show_edit_checklist_item_page(id):
    """Display edit checklist item page"""
    if session.get("user_email"):
        item = crud.get_checklist_item_by_id(id)
        user = crud.get_user_by_email(session["user_email"])
        items = user.checklist_items
        count = len(items) 
        return render_template("edit_checklist_item.html", 
                                id=item.item_id, 
                                question=item.question,
                                advice=item.advice,
                                position=item.order,
                                count=count)
    else:
        return redirect("/")

@app.route("/edit-checklist-item/<id>", methods=["POST"])
def edit_chcklist_item(id):
    """Edit Checklist Item"""
    user = crud.get_user_by_email(session["user_email"])
    item = crud.get_checklist_item_by_id(id)
    question = request.form.get("question")
    advice = request.form.get("advice")
    order = int(request.form.get("order"))
    crud.edit_checklist_item(user, item, question, advice, order)
    db.session.commit()
    flash(f"Edited {question}")
    return redirect("/edit-checklist")


@app.route("/remove-checklist-item/<id>")
def remove_checklist_item(id):
    """Remove item from checklist"""
    user = crud.get_user_by_email(session['user_email'])
    item = crud.get_checklist_item_by_id(id)
    crud.delete_checklist_item(user, item)
    db.session.commit()
    flash(f"Removed {item.question}")
    return redirect("/edit-checklist")

@app.route("/account-preferences")
def show_account_preferences():
    """Show account preferences page"""
    if session.get("user_email"):
        user = crud.get_user_by_email(session['user_email'])
        return render_template("account_preferences.html",
                                name=user.name,
                                email=user.email,
                                zipcode=user.zipcode,
                                phone=user.phone)
    else:
        return redirect("/")

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
    if "user_email" in session:
        print("USER_EMAIL")
        user = crud.get_user_by_email(session["user_email"])
        data = weather.get_walking_weather(zipcode, user)
    else:
        if crud.get_user_by_email(EMAIL) != None:
            print("NOT NONE")
            crud.update_user_account_preferences(crud.get_user_by_email(EMAIL), NAME, EMAIL, zipcode, "")
            user = crud.get_user_by_email(EMAIL)
        else:
            user, checklist, activities = crud.create_user(EMAIL, PASSWORD, NAME, zipcode)
            db.session.add(user)
            db.session.add_all(checklist)
            db.session.add_all(activities)
        db.session.commit()
        data = weather.get_walking_weather(zipcode, user)
    return jsonify(data)


if __name__ == "__main__":
    connect_to_db(app)
    
    app.run(host="0.0.0.0", debug=True)

    