CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    role TEXT NOT NULL DEFAULT 'työntekijä'
        CHECK(role IN ('admin', 'hallinnoitsija', 'työntekijä'))
);

CREATE TABLE shifts (
    id INTEGER PRIMARY KEY,
    location TEXT NOT NULL,
    duration INTEGER NOT NULL,
    shift_date DATE NOT NULL,
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE classification_types (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE classifications (
    id INTEGER PRIMARY KEY,
    type_id INTEGER NOT NULL REFERENCES classification_types(id),
    name TEXT NOT NULL,
    UNIQUE(type_id, name)
);

CREATE TABLE shift_classifications (
    shift_id INTEGER NOT NULL REFERENCES shifts(id) ON DELETE CASCADE,
    classification_id INTEGER NOT NULL REFERENCES classifications(id),
    PRIMARY KEY (shift_id, classification_id)
);

CREATE TABLE shift_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shift_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    note TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shift_id) REFERENCES shifts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO classification_types (name) VALUES ('Sijainti');
INSERT INTO classification_types (name) VALUES ('Tehtävä');
INSERT INTO classifications (type_id, name) VALUES (1, 'Etänä');
INSERT INTO classifications (type_id, name) VALUES (1, 'Paikanpäällä');
INSERT INTO classifications (type_id, name) VALUES (2, 'Koulutustehtävät');
INSERT INTO classifications (type_id, name) VALUES (2, 'Myynti');
INSERT INTO classifications (type_id, name) VALUES (2, 'Asiakaspalvelu');