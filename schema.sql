CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
)

CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
)

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    author_id INTEGER REFERENCES authors,
    title TEXT,
    year TEXT,
    description TEXT
)

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT
)

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    book_id  INTEGER REFERENCES books,
    comment TEXT
)

CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    book_id INTEGER REFERENCES books,
    rating INTEGER
)
