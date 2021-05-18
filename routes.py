from app import app
from flask import render_template
import books_functions

@app.route("/")
def index():
    return render_template("index.html", books=books_functions.get_all_books())
