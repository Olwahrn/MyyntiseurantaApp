import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import shifts
import users
import secrets
from flask import abort, request, session
app = Flask(__name__)
app.secret_key = config.secret_key

def check_csrf():
    if session.get("csrf_token") != request.form.get("csrf_token"):
        abort(403)

@app.route("/")
def index():
    shift_list = shifts.get_shifts()
    return render_template("index.html", shifts = shift_list)

@app.route("/find_shift")
def find_shift():
    query = request.args.get("query")
    if query:
        results = shifts.find_shifts(query)
    else:
        query = ""
        results = []
    return render_template("find_shift.html", query = query, results=results)

@app.route("/shift/<int:shift_id>")
def show_shift(shift_id):
    shift = shifts.get_shift(shift_id)
    classifications = shifts.get_classifications_for_shift(shift_id)
    notes = shifts.get_shift_notes(shift_id)

    return render_template("show_shift.html", shift=shift, classifications=classifications, notes=notes)

@app.route("/new_shift")
def new_shift():
    classifications = shifts.get_classifications_grouped()
    return render_template("new_shift.html", classifications=classifications)
    
@app.route("/create_new_shift", methods=["POST"])
def create_shift():
    check_csrf()
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    location = request.form["location"]
    duration = int(request.form["duration"])
    date = request.form["date"]
    user_id = session["user_id"]

    shift_id = shifts.add_shift(location, duration, date, user_id)

    selected_classifications = request.form.getlist("classifications")
    for classification_id in selected_classifications:
        shifts.add_classification_to_shift(shift_id, int(classification_id))

    return redirect("/")

@app.route("/update_shift", methods=["POST"])
def update_shift():
    check_csrf()
    shift_id = request.form["shift_id"]
    location = request.form["location"]
    duration = int(request.form["duration"])
    date = request.form["date"]

    shifts.update_shift(shift_id, location, duration, date)
    return redirect("/shift/" + str(shift_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/edit_shift/<int:shift_id>")
def edit_shift(shift_id):
    shift = shifts.get_shift(shift_id)
    if not users.can_edit_shift(session["user_id"], shift["user_id"]):
        return "Sinulla ei ole muokkausoikeuksia tähän vuoroon", 403
    return render_template("edit_shift.html", shift=shift)

@app.route("/remove_shift/<int:shift_id>",  methods=["GET", "POST"])
def remove_shift(shift_id):
    if request.method == "GET":
        shift = shifts.get_shift(shift_id)
        return render_template("remove_shift.html", shift=shift)
    
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            shifts.remove_shift(shift_id)
            return redirect("/")
        else:
            return redirect("/shift/" + str(shift_id))
        
@app.route("/user/<int:user_id>")
def user_page(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    user = db.query(sql, [user_id])[0]

    sql_stats = """SELECT COUNT(*) as shift_count, 
                          SUM(duration) as total_duration 
                   FROM shifts 
                   WHERE user_id = ?"""
    stats = db.query(sql_stats, [user_id])[0]

    sql_shifts = """SELECT id, location, duration, shift_date 
                    FROM shifts 
                    WHERE user_id = ? 
                    ORDER BY shift_date DESC"""
    user_shifts = db.query(sql_shifts, [user_id])
    return render_template("user.html", user=user, stats=stats, shifts=user_shifts)

@app.route("/create", methods=["POST"])
@app.route("/create", methods=["POST"])
def create():
    check_csrf()
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if len(username) < 3:
        return render_template("register.html", error="Käyttäjätunnuksen tulee olla vähintään 3 merkkiä pitkä")
    
    if len(password1) < 3:
        return render_template("register.html", error="Salasanan tulee olla vähintään 3 merkkiä pitkä")
    
    if password1 != password2:
        return render_template("register.html", error="Salasanat eivät täsmää")
    
    if users.username_exists(username):
        return render_template("register.html", error="Käyttäjänimi varattu")

    password_hash = generate_password_hash(password1)
    users.create_user(username, password_hash)

    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form["username"]
    password = request.form["password"]

    user = users.get_user_by_username(username)
    if not user:
        return render_template("login.html", error="Käyttäjää ei löytynyt")
    
    if check_password_hash(user["password_hash"], password):
        session["user_id"] = user["id"]
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    else:
        return render_template("login.html", error="Väärä käyttäjätunnus tai salasana")
    
@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")

@app.route("/add_note/<int:shift_id>", methods=["POST"])
def add_note(shift_id):
    check_csrf()
    note = request.form["note"]
    user_id = session["user_id"]

    sql = """INSERT INTO shift_notes (shift_id, user_id, note)
             VALUES (?, ?, ?)"""
    db.execute(sql, [shift_id, user_id, note])

    return redirect(f"/shift/{shift_id}")
