from app import app
from flask import render_template, redirect, request
import books_functions, users_functions

@app.route("/")
def index():
    return render_template("index.html", books=books_functions.get_all_books())

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users_functions.log_in(username, password):
            return redirect("/")
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)

@app.route("/signin", methods=["GET", "POST"])
def signin():
    error = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users_functions.sign_in(username, password, 0):
            return redirect("/")
        else:
            error = "Invalid input"

    return render_template("signin.html", error=error)

@app.route("/logout")
def logout():
    users_functions.log_out()
    return redirect("/")

@app.route("/book/<id>")
def book(id):
    book = books_functions.get_book(id)
    return render_template("book.html", book=book)