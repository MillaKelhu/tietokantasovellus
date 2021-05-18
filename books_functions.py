from db import db

def get_all_books():
    sql = "SELECT b.id, b.title, a.name FROM books b, authors a WHERE b.author_id=a.id"
    return db.session.execute(sql).fetchall()

def add_books():
    pass