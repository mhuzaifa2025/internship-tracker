from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("applications.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    if request.method == "POST":
        company = request.form.get("company")
        status = request.form.get("status")
        cursor.execute(
            "INSERT INTO applications (company, status) VALUES (?, ?)",
            (company, status)
        )
        conn.commit()

    cursor.execute("SELECT * FROM applications")
    applications = cursor.fetchall()
    conn.close()

    return render_template("index.html", applications=applications)

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    app.run()






