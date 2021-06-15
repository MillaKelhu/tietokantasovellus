from db import db
import booklist_functions
import genre_functions
import review_functions

def get_all_books():
    sql = """SELECT b.id, b.title, a.name 
             FROM books b, authors a 
             WHERE b.author_id=a.id
             ORDER BY a.name ASC, b.title ASC"""
    return db.session.execute(sql).fetchall()

def get_book(book_id):
    sql = """SELECT b.id, b.title, a.name, b.year, b.description 
             FROM books b, authors a 
             WHERE b.id=:id 
             AND b.author_id=a.id"""
    return db.session.execute(sql, {"id":int(book_id)}).fetchone()

def add_book(author_name, title, year, description):
    author = author_exists(author_name)
    if author:
        if book_exists(author[0], title) is None:
            sql = """INSERT INTO books(author_id, title, year, description)
                     VALUES (:author_id, :title, :year, :description)"""
            db.session.execute(sql, {"author_id":author[0], "title":title, "year": year, "description":description})
            db.session.commit()
            return True
    return False

def delete_book(book_id):
    booklist_functions.book_deleted(book_id)
    genre_functions.book_deleted(book_id)
    review_functions.book_deleted(book_id)
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

def get_all_authors():
    sql = """SELECT name 
             FROM authors
             ORDER BY name ASC"""
    return db.session.execute(sql).fetchall()

def book_exists(author_id, title):
    sql = """SELECT id
             FROM books
             WHERE title=:title
             AND author_id=:author_id"""
    return db.session.execute(sql, {"title":title, "author_id":author_id}).fetchone()

def search_books(title, author, earliest_year, latest_year, description, genrestring=None, minrating=0):
    if genrestring:
        genres = genre_functions.tag_handler(genrestring)
        sql = """SELECT b.id, b.title, a.name
             FROM books b, authors a
             WHERE b.title LIKE :title_query
             AND a.name LIKE :author_query
             AND b.author_id=a.id
             AND b.year BETWEEN :earliest_year_query AND :latest_year_query
             AND b.description LIKE :description_query
             AND :genres <@ ARRAY(SELECT g.name 
                                         FROM genres g, genrebooks x
                                         WHERE g.id=x.genre_id
                                         AND b.id=x.book_id)
             AND :minrating <= (SELECT COALESCE(ROUND(AVG(r.rating), 2), 0) 
                                FROM books b LEFT JOIN ratings r ON b.id=r.book_id 
                                WHERE book_id=b.id)"""
        return db.session.execute(sql, {
        "title_query":"%"+title+"%",
        "author_query":"%"+author+"%",
        "earliest_year_query":earliest_year,
        "latest_year_query":latest_year,
        "description_query":"%"+description+"%",
        "genres":genres,
        "minrating":minrating
        }).fetchall()
    sql = """SELECT b.id, b.title, a.name
         FROM books b, authors a
         WHERE b.title LIKE :title_query
         AND a.name LIKE :author_query
         AND b.author_id=a.id
         AND b.year BETWEEN :earliest_year_query AND :latest_year_query
         AND b.description LIKE :description_query
         AND :minrating <= (SELECT COALESCE(ROUND(AVG(r.rating), 2), 0) 
                            FROM books b LEFT JOIN ratings r ON b.id=r.book_id 
                            WHERE book_id=b.id)"""
    return db.session.execute(sql, {
    "title_query":"%"+title+"%",
    "author_query":"%"+author+"%",
    "earliest_year_query":earliest_year,
    "latest_year_query":latest_year,
    "description_query":"%"+description+"%",
    "minrating":minrating
    }).fetchall()