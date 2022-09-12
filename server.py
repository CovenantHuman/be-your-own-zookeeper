"""Server for self care app."""

from flask import(Flask, render_template, request, flash, session, redirect, jsonify)
from jinja2 import StrictUndefined
import requests
import os

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
OPEN_WEATHER_KEY = os.environ["OPEN_WEATHER_KEY"]

@app.route("/")
def homepage():
    """Show homepage"""
    return render_template("homepage.html")

@app.route("/zip-form")
def get_weather():
    """Take in the zipcode and gets the weather"""
    zipcode = request.args.get("zipcode")
    print("ZIPCODE IS", zipcode)
    zip_with_country_code = zipcode + ",us"
    url = "https://api.openweathermap.org/data/2.5/weather"
    payload = {"zip": zip_with_country_code, "appid": OPEN_WEATHER_KEY}
    response = requests.get(url, params=payload)
    data = response.json()
    print(data)
    return jsonify(data)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)