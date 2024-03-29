DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTs users;

CREATE TABLE posts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created DATE NOT NULL DEFAULT CURRENT_DATE,
    author TEXT NOT NULL DEFAULT 'Tim',
    title TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    body TEXT NOT NULL
);

CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    handle TEXT NOT NULL,
    userpass TEXT NOT NULL
);