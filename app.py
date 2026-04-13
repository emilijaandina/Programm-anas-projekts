from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)

def izveidot_db():
    conn = sqlite3.connect("datubaze.db")
    cursor = conn.cursor()
    cursor.execute ("""
    CREATE TABLE IF NOT EXISTS "users"(
    "id" INTEGER,
    "username" TEXT,
    "password" TEXT,
    PRIMARY KEY("id")
    )
    """)
    conn.commit()
    conn.close()
izveidot_db()

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        #print(username)
        #print(password)
        conn = sqlite3.connect("datubaze.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    return render_template("login.html")

if __name__ =="__main__":
    app.run(debug=True)