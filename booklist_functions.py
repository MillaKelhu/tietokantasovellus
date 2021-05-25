from db import db
from flask import session

def add_to_booklist(book_id):
    if book_in_list(book_id):
        return
    sql = """INSERT INTO booklist(user_id, book_id, status)
             VALUES(:user_id, :book_id, 0)"""
    db.session.execute(sql, {"user_id":session["user_id"], "book_id":book_id})
    db.session.commit()

def get_booklist():
    sql = """SELECT b.id, b.title, a.name, l.status
             FROM books b, authors a, booklist l
             WHERE l.user_id=:user_id
             AND l.book_id=b.id
             AND b.author_id=a.id"""
    return db.session.execute(sql, {"user_id":session["user_id"]}).fetchall()

def book_in_list(book_id):
    sql = """SELECT *
             FROM booklist
             WHERE user_id=:user_id
             AND book_id=:book_id"""
    return db.session.execute(sql, {"user_id":session["user_id"], "book_id":book_id}).fetchone()

def book_read(book_id):
    sql = """SELECT *
             FROM booklist
             WHERE user_id=:user_id
             AND book_id=:book_id
             AND status=2"""
    return db.session.execute(sql, {"user_id":session["user_id"], "book_id":book_id}).fetchone()

def mark_as_currently_reading(book_id):
    sql = """UPDATE booklist
             SET status=1
             WHERE book_id=:book_id
             AND user_id=:user_id"""
    db.session.execute(sql, {"book_id":book_id, "user_id":session["user_id"]})
    db.session.commit()

def mark_as_read(book_id):
    sql = """UPDATE booklist
             SET status=2
             WHERE book_id=:book_id
             AND user_id=:user_id"""
    db.session.execute(sql, {"book_id":book_id, "user_id":session["user_id"]})
    db.session.commit()
    
def book_deleted(book_id):
    sql = """DELETE FROM booklist
             WHERE book_id=:book_id"""
    db.session.execute(sql, {"book_id":book_id})
    db.session.commit()