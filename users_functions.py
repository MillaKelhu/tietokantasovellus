from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def log_in(username, password):
    sql = "SELECT * FROM users WHERE username=:username"
    user = db.session.execute(sql, {"username":username}).fetchone()
    if user:
        hash_value = user[2]
        if check_password_hash(hash_value, password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["user_role"] = user[3]
            return True
    
    return False

def log_out():
    del session["user_id"]
    del session["username"]
    del session["user_role"]
    return True

def sign_in(username, password, role):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users(username, password, role) VALUES (:username, :password, :role)"
    try:
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
        return True
    except:
        return False