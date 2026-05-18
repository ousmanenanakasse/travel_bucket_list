from datetime import datetime

from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_db_connection, init_db
from logic import is_valid_budget, is_valid_priority, is_valid_status


app = Flask(__name__)
app.secret_key = "my_secret_key"


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/init-db")
def initialize_database():
    init_db()
    return "Database initialized successfully!"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()

        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
        except:
            conn.close()
            return "Username already exists."

        conn.close()
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))

        return "Invalid username or password."

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    destinations = conn.execute(
        "SELECT * FROM destinations WHERE user_id = ? ORDER BY id DESC",
        (session["user_id"],)
    ).fetchall()

    conn.close()

    return render_template("dashboard.html", destinations=destinations)


@app.route("/add", methods=["GET", "POST"])
def add_destination():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        country = request.form["country"]
        reason = request.form["reason"]
        priority = request.form["priority"]
        status = request.form["status"]
        budget = float(request.form["budget"])
        created_at = datetime.now().strftime("%d %B %Y - %H:%M")

        if not is_valid_budget(budget):
            return "Budget cannot be negative."

        if not is_valid_priority(priority):
            return "Invalid priority."

        if not is_valid_status(status):
            return "Invalid status."

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO destinations
            (name, country, reason, priority, status, budget, created_at, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                country,
                reason,
                priority,
                status,
                budget,
                created_at,
                session["user_id"]
            )
        )

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("add_destination.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_destination(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    destination = conn.execute(
        "SELECT * FROM destinations WHERE id = ? AND user_id = ?",
        (id, session["user_id"])
    ).fetchone()

    if destination is None:
        conn.close()
        return "Destination not found or access denied."

    if request.method == "POST":
        name = request.form["name"]
        country = request.form["country"]
        reason = request.form["reason"]
        priority = request.form["priority"]
        status = request.form["status"]
        budget = float(request.form["budget"])

        if not is_valid_budget(budget):
            conn.close()
            return "Budget cannot be negative."

        if not is_valid_priority(priority):
            conn.close()
            return "Invalid priority."

        if not is_valid_status(status):
            conn.close()
            return "Invalid status."

        conn.execute(
            """
            UPDATE destinations
            SET name = ?, country = ?, reason = ?, priority = ?, status = ?, budget = ?
            WHERE id = ? AND user_id = ?
            """,
            (
                name,
                country,
                reason,
                priority,
                status,
                budget,
                id,
                session["user_id"]
            )
        )

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    conn.close()

    return render_template("edit_destination.html", destination=destination)


@app.route("/delete/<int:id>")
def delete_destination(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM destinations WHERE id = ? AND user_id = ?",
        (id, session["user_id"])
    )

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)