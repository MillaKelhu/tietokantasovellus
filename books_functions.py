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

def add_book(author_id, title, year, description):
    if author_exists(author_id):
        if book_exists(author_id, title) is None:
            sql = """INSERT INTO books(author_id, title, year, description)
                     VALUES (:author_id, :title, :year, :description)"""
            db.session.execute(sql, {"author_id":author_id, "title":title, "year": year, "description":description})
            db.session.commit()
            return True
    return False

def author_exists(author_id):
    sql = """SELECT *
             FROM authors
             WHERE id=:author_id"""
    return db.session.execute(sql, {"author_id":author_id}).fetchone()

def book_exists(author_id, title):
    sql = """SELECT *
                 FROM books
                 WHERE title=:title
                 AND author_id:=author_id"""
    return db.session.execute(sql, {"title":title, "author_id":author_id}).fetchone()