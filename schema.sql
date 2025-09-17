CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE shifts (
    id INTEGER PRIMARY KEY,
    location TEXT NOT NULL,
    duration INTEGER NOT NULL,
    shift_date DATE NOT NULL,
    user_id INTEGER REFERENCES users
);