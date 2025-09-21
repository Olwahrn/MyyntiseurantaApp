import db 
def add_shift(location, duration, date, user_id):
    sql = """INSERT INTO users (location, duration, date, user_id) VALUES (?, ?, ?, ?)"""
    db.execute(sql, [location, duration, date, user_id])