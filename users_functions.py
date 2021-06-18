from db import db
from flask import session, request, abort
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
import booklist_functions
import review_functions

def log_in(username, password):
    sql = """SELECT id, username, password, role 
             FROM users 
             WHERE username=:username"""
    user = db.session.execute(sql, {"username":username}).fetchone()
    if user:
        hash_value = user[2]
        if check_password_hash(hash_value, password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["user_role"] = user[3]
            session["csrf_token"] = secrets.token_hex(16)

            return True
    
    return False

def log_out():
    del session["user_id"]
    del session["username"]
    del session["user_role"]
    return True

def sign_in(username, password, role):
    hash_value = generate_password_hash(password)
    sql = """INSERT INTO users(username, password, role) 
    VALUES (:username, :password, :role)"""
    try:
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
        return True
    except:
        return False

def get_user():
    try:
        user = (session["user_id"], session["username"], session["user_role"])
        return user
    except KeyError:
        return None

def admin():
    return bool(session["user_role"]==1)

def get_all_users():
    sql = """SELECT id, username 
             FROM users"""
    return db.session.execute(sql).fetchall()

def get_user_by_id(id):
    sql = """SELECT id, username, role 
             FROM users
             WHERE id=:id"""
    return db.session.execute(sql, {"id":id}).fetchone()

def revoke_rights(id):
    sql = """UPDATE users
             SET role = -1
             WHERE id =:id"""
    db.session.execute(sql, {"id":id})
    db.session.commit()

def return_rights(id):
    sql = """UPDATE users
             SET role = 0
             WHERE id =:id"""
    db.session.execute(sql, {"id":id})
    db.session.commit()

def delete_user(id):
    booklist_functions.user_deleted(id)
    review_functions.user_deleted(id)
    sql = """DELETE FROM users
             WHERE id =:id"""
    db.session.execute(sql, {"id":id})
    db.session.commit()

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
