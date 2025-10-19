from db import query, execute

def get_user_role(user_id):
    sql = "SELECT role FROM users WHERE id = ?"
    result = query(sql, [user_id])
    return result[0]["role"] if result else None

def is_admin(user_id):
    return get_user_role(user_id) == "admin"

def is_manager(user_id):
    return get_user_role(user_id) == "manager"

def can_edit_shift(current_user_id, shift_user_id):
    role = get_user_role(current_user_id)
    if role in ["admin", "manager"]:
        return True
    return current_user_id == shift_user_id

def create_user(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    execute(sql, [username, password_hash])

def get_user_by_username(username):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = query(sql, [username])
    return result[0] if result else None

def username_exists(username):
    sql = "SELECT id FROM users WHERE username = ?"
    result = query(sql, [username])
    return len(result) > 0