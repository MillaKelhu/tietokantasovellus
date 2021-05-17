from app import app
from flask import render_template
import books, users

@app.route("/")
def index():
    return render_template("index.html")