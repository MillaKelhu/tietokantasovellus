from app import app
from flask import render_template, redirect, request
import books_functions, users_functions, booklist_functions, review_functions, genre_functions

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

@app.route("/book/<id>", methods=["GET", "POST"])
def book(id):
    in_list = False
    read = False
    if users_functions.get_user():
        if booklist_functions.book_in_list(id):
            in_list = True

        if booklist_functions.book_read(id):
            read = True

            if request.method=="POST":
                if request.form["submit"] == "Add to booklist":
                    status = request.form["booklist"]
                    booklist_functions.add_to_booklist(id, status)

                if request.form["submit"] == "Rate book":
                    rate = request.form["rating"]
                    review_functions.add_rating(id, rate)
    
                if request.form["submit"] == "Write a comment":
                    comment = request.form["comment"]
                    if comment != "":
                        review_functions.add_comment(id, comment)

    book = books_functions.get_book(id)
    rating = review_functions.get_rating(id)[0]

    if rating==None:
        rating = "–"

    comments = review_functions.get_comments(id)
    genres = genre_functions.get_genres(id)

    return render_template("book.html", book=book, in_list=in_list, read=read, rating=rating, comments=comments, genres=genres)

@app.route("/book/<id>/delete", methods=["GET", "POST"])
def book_delete(id):
    if users_functions.admin():
        book = books_functions.get_book(id)

        if request.method=="POST":
            books_functions.delete_book(id)
            return redirect("/")
        
        return render_template("bookdelete.html", book=book)

    return redirect(f"/book/{id}")

@app.route("/book/<id>/modify", methods=["GET", "POST"])
def book_modify(id):
    if users_functions.admin():
        book = books_functions.get_book(id)
        genrelist = genre_functions.get_genres(id)
        genres = ""
        for nametuple in genrelist:
            genres += ", " + nametuple[1]
        genres = genres[2:]

        if request.method=="POST":
            title = request.form["title"]
            author = request.form["author"]
            year = request.form["year"]
            description = request.form["description"]
            genres = request.form["genres"]
            if title != "" and author != "" and year != "" and description != "" and genres != "":
                books_functions.modify_book(id, author, title, year, description)
                genrelist = genre_functions.handle_tags(genres)
                for genre in genrelist:
                    genre_functions.assign_genre(id, genre)
            return redirect(f"/book/{id}")

        return render_template("bookmodify.html", book=book, genres=genres)
    
    return redirect(f"/book/{id}")

@app.route("/profile")
def profile():
    user = users_functions.get_user()
    if users_functions.get_user():
        return render_template("profile.html", user=user)
    else:
        return redirect("/")

@app.route("/profile/booklist")
def profile_booklist():
    if users_functions.get_user():
        booklist = booklist_functions.get_booklist()
        return render_template("booklist.html", booklist=booklist)
    else:
        return redirect("/")

@app.route("/profile/booklist/update", methods=["GET", "POST"])
def profile_booklist_update():
    if users_functions.get_user():

        if request.method == "POST":
            new_currently_reading = request.form.getlist("reading")
            new_read = request.form.getlist("read")
            for id in new_currently_reading:
                booklist_functions.mark_as_currently_reading(id)
            for id in new_read:
                booklist_functions.mark_as_read(id)
            return redirect("/profile/booklist")

        booklist = booklist_functions.get_booklist()
        return render_template("booklist_update.html", booklist=booklist)
    else:
        return redirect("/")

@app.route("/addbook", methods=["GET", "POST"])
def add_book():
    if users_functions.admin():

        if request.method == "POST":
            title = request.form["title"]
            author = request.form["author"]
            year = request.form["year"]
            description = request.form["description"]
            genres = request.form["genres"]
            if title != "" and author != "" and year != "" and description != "" and genres != "":
                books_functions.add_book(author, title, year, description)
                genrelist = genre_functions.handle_tags(genres)
                author_id = books_functions.author_exists(author)[0]
                book_id = books_functions.book_exists(author_id, title)[0]
                for genre in genrelist:
                    genre_functions.assign_genre(book_id, genre)

            return redirect("/")

        return render_template("addbook.html")
    else:
        return redirect("/")

@app.route("/addauthor", methods=["GET", "POST"])
def add_author():
    if users_functions.admin():

        if request.method == "POST":
            name = request.form["name"]
            books_functions.add_author(name)
            return redirect("/")

        return render_template("addauthor.html")
    else:
        return redirect("/")

@app.route("/addgenre", methods=["GET", "POST"])
def add_genre():
    if users_functions.admin():

        if request.method == "POST":
            name = request.form["name"]
            genre_functions.add_genre(name)
            return redirect("/")

        return render_template("addgenre.html")
    else:
        return redirect("/")

@app.route("/genres/<id>")
def genre(id):
    genre = genre_functions.get_genre_name(id)
    books = genre_functions.get_genre_books(id)

    return render_template("genre.html", genre=genre, books=books)

@app.route("/search", methods=["GET", "POST"])
def search():
    books = books_functions.get_all_books()

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        year = request.form["year"]
        description = request.form["description"]
        if title == "":
            title = "%"
        if author == "":
            author = "%"
        if year == "":
            year = "%"
        if description == "":
            description = "%"
        books = books_functions.search_books(title, author, year, description)

    return render_template("search.html", books=books)