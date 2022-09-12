"""Server for self care app."""

from flask import(Flask, render_template, request, flash, session, redirect)
from jinja2 import StrictUndefined
import os

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
OPEN_WEATHER_KEY = os.environ["OPEN_WEATHER_KEY"]

@app.route("/")
def homepage():
    """Show homepage"""
    return render_template("homepage.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)