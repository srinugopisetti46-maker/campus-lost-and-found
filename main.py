from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"
DB = "campus_lost_found.db"

def get_db():
    return sqlite3.connect(DB)

# ---------------- LOGIN PAGES ----------------

@app.route("/")
def home():
    return render_template("combined.html")

@app.route("/login_user", methods=["POST"])
def login_user():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND role='user'", (username,))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user[2], password):
        session["user"] = user[1]
        session["role"] = "user"
        return redirect("/user")
    else:
        flash("Invalid User Credentials")
        return redirect("/")

@app.route("/login_admin", methods=["POST"])
def login_admin():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND role='admin'", (username,))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user[2], password):
        session["user"] = user[1]
        session["role"] = "admin"
        return redirect("/admin")
    else:
        flash("Invalid Admin Credentials")
        return redirect("/")

# ---------------- USER ----------------

@app.route("/user")
def user():
    if session.get("role") != "user":
        return redirect("/")
    return render_template("combined.html", page="user")

@app.route("/report_lost", methods=["POST"])
def report_lost():
    item = request.form["item"]
    details = request.form["details"]
    place = request.form["place"]
    contact = request.form["contact"]

    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO items (item, details, place, status, contact) VALUES (?, ?, ?, 'lost', ?)",
              (item, details, place, contact))
    conn.commit()
    conn.close()

    flash("Lost item reported successfully!")
    return redirect("/user")

@app.route("/report_found", methods=["POST"])
def report_found():
    item = request.form["item"]
    details = request.form["details"]
    place = request.form["place"]
    contact = request.form["contact"]

    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO items (item, details, place, status, contact) VALUES (?, ?, ?, 'found', ?)",
              (item, details, place, contact))
    conn.commit()
    conn.close()

    flash("Found item reported successfully!")
    return redirect("/user")

# ---------------- ADMIN ----------------

@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect("/")

    conn = get_db()
    c = conn.cursor()

    lost = c.execute("SELECT * FROM items WHERE status='lost'").fetchall()
    found = c.execute("SELECT * FROM items WHERE status='found'").fetchall()

    matches = []
    for l in lost:
        for f in found:
            if l[1].lower() in f[1].lower() or f[1].lower() in l[1].lower():
                matches.append((l, f))

    conn.close()
    return render_template("combined.html", page="admin", lost=lost, found=found, matches=matches)

# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)