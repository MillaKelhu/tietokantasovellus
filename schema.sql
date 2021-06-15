CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    author_id INTEGER REFERENCES authors,
    title TEXT,
    year INTEGER,
    description TEXT
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    book_id  INTEGER REFERENCES books,
    comment TEXT
);

CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    book_id INTEGER REFERENCES books,
    rating INTEGER
);

CREATE TABLE booklist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    book_id INTEGER REFERENCES books,
    status INTEGER
);

CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE genrebooks (
    id SERIAL PRIMARY KEY,
    genre_id INTEGER REFERENCES genres,
    book_id INTEGER REFERENCES books
);