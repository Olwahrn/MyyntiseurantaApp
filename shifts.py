import db 
from collections import defaultdict
def add_shift(location, duration, date, user_id):
    sql = """INSERT INTO shifts (location, duration, shift_date, user_id)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [location, duration, date, user_id])
    return db.last_insert_id()

def get_shifts():
    sql = "SELECT id, location, shift_date, user_id FROM shifts ORDER BY id DESC"
    return db.query(sql)

def get_shift(shift_id):
    sql = """SELECT shifts.id,
                    shifts.location,
                    shifts.duration,
                    shifts.shift_date,
                    users.id user_id,
                    users.username
            FROM shifts, users
            WHERE shifts.user_id = users.id AND
                  shifts.id = ?"""
    return db.query(sql, [shift_id])[0]

def update_shift(shift_id, location, duration, date):
    sql = """UPDATE shifts SET location = ?,
                                duration = ?,
                                shift_date = ?
                                WHERE id = ? """
    db.execute(sql, [location, duration, date, shift_id])

def remove_shift(shift_id):
    sql = "DELETE FROM shifts WHERE id = ?"
    db.execute(sql, [shift_id])

def find_shifts(query):
    sql = """SELECT id, location
            FROM shifts
            WHERE location LIKE ?
            ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like])

def add_classification_to_shift(shift_id, classification_id):
    sql = """INSERT OR IGNORE INTO shift_classifications (shift_id, classification_id) VALUES (?, ?)"""
    db.execute(sql, [shift_id, classification_id])

def get_classifications_for_shift(shift_id):
    sql = """SELECT c.id, c.name, ct.name as type
             FROM classifications c
             JOIN classification_types ct ON c.type_id = ct.id
             JOIN shift_classifications sc ON sc.classification_id = c.id
             WHERE sc.shift_id = ?"""
    return db.query(sql, [shift_id])

def get_all_classifications():
    sql = """SELECT c.id, c.name, ct.name as type
             FROM classifications c
             JOIN classification_types ct ON c.type_id = ct.id"""
    return db.query(sql)

def get_classifications_grouped():
    all_classes = get_all_classifications()
    grouped = defaultdict(list)
    for c in all_classes:
        grouped[c["type"]].append(c)
    return grouped