from db import db
import booklist_functions
import genre_functions

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

def add_book(author_name, title, year, description):
    author_id = author_exists(author_name)[0]
    if author_id:
        if book_exists(author_id, title) is None:
            sql = """INSERT INTO books(author_id, title, year, description)
                     VALUES (:author_id, :title, :year, :description)"""
            db.session.execute(sql, {"author_id":author_id, "title":title, "year": year, "description":description})
            db.session.commit()
            return True
    return False

def delete_book(book_id):
    booklist_functions.book_deleted(book_id)
    genre_functions.book_deleted(book_id)
    sql = """DELETE FROM books
             WHERE id=:book_id"""
    db.session.execute(sql, {"book_id":book_id})
    db.session.commit()

def modify_book(book_id, author_name, title, year, description):
    author_id = author_exists(author_name)[0]
    if author_id:
        sql = """UPDATE books
                 SET author_id=:author_id,
                     title=:title,
                     year=:year,
                     description=:description
                 WHERE id=:book_id"""
        db.session.execute(sql, {"book_id":book_id, "author_id":author_id, "title":title, "year": year, "description":description})
        db.session.commit()

def author_exists(author_name):
    sql = """SELECT id
             FROM authors
             WHERE name=:author_name"""
    return db.session.execute(sql, {"author_name":author_name}).fetchone()

def add_author(author_name):
    sql = """INSERT INTO authors(name)
             VALUES (:author_name)"""
    try:
        db.session.execute(sql, {"author_name":author_name})
        db.session.commit()
        return True
    except:
        return False

def book_exists(author_id, title):
    sql = """SELECT *
             FROM books
             WHERE title=:title
             AND author_id=:author_id"""
    return db.session.execute(sql, {"title":title, "author_id":author_id}).fetchone()

def search_books(title, author, year, description):
    sql = """SELECT b.id, b.title, a.name
             FROM books b, authors a
             WHERE b.title LIKE :title_query
             AND a.name LIKE :author_query
             AND b.author_id=a.id
             AND b.year LIKE :year_query
             AND b.description LIKE :description_query"""
    return db.session.execute(sql, {
        "title_query":"%"+title+"%",
        "author_query":"%"+author+"%",
        "year_query":year,
        "description_query":"%"+description+"%",
    }).fetchall()