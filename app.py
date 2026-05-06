from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "testkey"

# DB savienojums
def get_db():
    conn = sqlite3.connect("datubaze.db")
    conn.row_factory = sqlite3.Row
    return conn

# DB izveide
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        user_id INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

# HOME
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT text FROM recipes WHERE user_id = ?",
        (session["user_id"],)
    )
    recipes = cursor.fetchall()

    conn.close()

    return render_template("home.html", recipes=recipes)

# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
        except:
            return "Username jau eksistē"

        conn.close()

        return redirect("/login")

    return render_template("register.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password = ?",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            return redirect("/")
        else:
            return "Nepareizs login"

    return render_template("login.html")

# ADD RECIPE
@app.route("/add", methods=["POST"])
def add():
    if "user_id" in session:
        text = request.form["recipe"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO recipes (text, user_id) VALUES (?, ?)",
            (text, session["user_id"])
        )

        conn.commit()
        conn.close()

    return redirect("/")

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)