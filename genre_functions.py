from db import db

def add_genre(name):
    sql = """INSERT INTO genres(name)
             VALUES (:name)"""
    try:
        db.session.execute(sql, {"name":name})
        db.session.commit()
        return True
    except:
        return False

def get_genre(name):
    sql = """SELECT id, name
             FROM genres
             WHERE name=:name"""
    return db.session.execute(sql, {"name":name}).fetchone()

def assign_genre(book_id, genre_name):
    genre = get_genre(genre_name)
    if genre_assigned(book_id, genre_name) is None and genre is not None:
        sql = """INSERT INTO genrebooks(genre_id, book_id)
                 VALUES (:genre_id, :book_id)"""
        db.session.execute(sql, {"genre_id":genre[0], "book_id":book_id})
        db.session.commit()

def genre_assigned(book_id, genre_name):
    genre = get_genre(genre_name)
    if genre:
        sql = """SELECT id, genre_id, book_id
                 FROM genrebooks
                 WHERE genre_id=:genre_id
                 AND book_id=:book_id"""
        return db.session.execute(sql, {"genre_id":genre[0], "book_id":book_id}).fetchone()

def book_deleted(book_id):
    sql = """DELETE FROM genrebooks
             WHERE book_id=:book_id"""
    db.session.execute(sql, {"book_id":book_id})
    db.session.commit()

def get_genres(book_id):
    sql = """SELECT g.id, g.name
             FROM genres g, genrebooks b
             WHERE g.id=b.genre_id
             AND b.book_id=:book_id
             ORDER BY g.name ASC"""
    return db.session.execute(sql, {"book_id":book_id}).fetchall()

def get_genre_name(genre_id):
    sql = """SELECT name
             FROM genres
             WHERE id=:id"""
    return db.session.execute(sql, {"id":genre_id}).fetchone()[0]

def get_genre_books(genre_id):
    sql = """SELECT b.id, b.title, a.name
             FROM books b, genrebooks g, authors a
             WHERE g.genre_id=:genre_id
             AND g.book_id=b.id
             AND b.author_id=a.id
             ORDER BY a.name ASC, b.title ASC"""
    return db.session.execute(sql, {"genre_id":genre_id}).fetchall()

def get_all_genres():
    sql = """SELECT name 
             FROM genres
             ORDER BY name ASC"""
    return db.session.execute(sql).fetchall()
    