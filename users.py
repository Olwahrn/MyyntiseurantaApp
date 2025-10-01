import db

def get_user_role(user_id):
    sql = "SELECT role FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
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