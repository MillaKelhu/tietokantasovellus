from booklist_functions import book_read
from db import db
from flask import session

def get_rating(book_id):
    sql = """SELECT ROUND(AVG(rating), 2)
             FROM ratings
             WHERE book_id=:book_id"""
    return db.session.execute(sql, {"book_id":book_id}).fetchone()

def add_rating(book_id, rating):
    if is_rated(book_id):
        return change_rating(book_id, rating)
    else:
        sql = """INSERT INTO ratings(user_id, book_id, rating)
                 VALUES(:user_id, :book_id, :rating)"""
        db.session.execute(sql, {"user_id":session["user_id"], "book_id":book_id, "rating":rating})
        db.session.commit()

def is_rated(book_id):
    sql = """SELECT *
             FROM ratings
             WHERE user_id=:user_id
             AND book_id=:book_id"""
    return db.session.execute(sql, {"user_id":session["user_id"], "book_id":book_id}).fetchone()
    
def change_rating(book_id, rating):
    sql = """UPDATE ratings
             SET rating=:rating
             WHERE user_id=:user_id
             AND book_id=:book_id"""
    db.session.execute(sql, {"user_id":session["user_id"], "book_id":book_id, "rating":rating})
    db.session.commit()

def get_comments(book_id):
    sql = """SELECT u.username, c.comment, c.id
             FROM users u, comments c
             WHERE c.book_id=:book_id
             AND c.user_id=u.id
             ORDER BY c.id DESC"""
    return db.session.execute(sql, {"book_id":book_id}).fetchall()

def add_comment(book_id, comment):
    sql = """INSERT INTO comments(user_id, book_id, comment)
             VALUES(:user_id, :book_id, :comment)"""
    db.session.execute(sql, {"user_id":session["user_id"], "book_id":book_id, "comment":comment})
    db.session.commit()

def delete_comment(comment_id):
    sql = """DELETE FROM comments
             WHERE id=:id"""
    db.session.execute(sql, {"id":comment_id})
    db.session.commit()