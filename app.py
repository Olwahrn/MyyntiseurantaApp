import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import shifts
app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    shift_list = shifts.get_shifts()
    return render_template("index.html", shifts = shift_list)

@app.route("/shift/<int:shift_id>")
def show_shift(shift_id):
    shift = shifts.get_shift(shift_id)
    return render_template("show_shift.html", shift=shift)

@app.route("/new_shift")
def new_shift():
    return render_template("new_shift.html")
    
@app.route("/create_new_shift", methods=["POST"])
def create_shift():
    location = request.form["location"]
    duration = int(request.form["duration"])
    date = request.form["date"]
    user_id = session["user_id"]

    shifts.add_shift(location, duration, date, user_id)
    return redirect("/")

@app.route("/update_shift", methods=["POST"])
def update_shift():
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
    return render_template("edit_shift.html", shift=shift)

@app.route("/remove_shift/<int:shift_id>",  methods=["GET", "POST"])
def remove_shift(shift_id):
    if request.method == "GET":
        shift = shifts.get_shift(shift_id)
        return render_template("remove_shift.html", shift=shift)
    
    if request.method == "POST":
        if "remove" in request.form:
            shifts.remove_shift(shift_id)
            return redirect("/")
        else:
            return redirect("/shift/" + str(shift_id))


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")

