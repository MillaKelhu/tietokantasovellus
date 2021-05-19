from db import db

def get_all_books():
    sql = """SELECT b.id, b.title, a.name 
    FROM books b, authors a 
    WHERE b.author_id=a.id"""
    return db.session.execute(sql).fetchall()

def get_book(book_id):
    sql = """SELECT b.id, b.title, a.name, b.year, b.description 
    FROM books b, authors a 
    WHERE b.id=:id 
    AND b.author_id=a.id"""
    return db.session.execute(sql, {"id":int(book_id)}).fetchone()

def add_books():
    pass