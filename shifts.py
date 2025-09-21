import db 
def add_shift(location, duration, date, user_id):
    sql = """INSERT INTO shifts (location, duration, shift_date, user_id) VALUES (?, ?, ?, ?)"""
    db.execute(sql, [location, duration, date, user_id])

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