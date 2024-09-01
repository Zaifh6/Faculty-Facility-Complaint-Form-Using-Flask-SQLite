from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_name = request.form.get("nm")
        last_name = request.form.get("lnm")
        email = request.form.get("em")
        msg = request.form.get("message")
        return redirect(url_for("add_info", name=user_name, l_name=last_name, mail=email, complaint=msg))
    else:
        return render_template("index.html")

@app.route("/<name>/<l_name>/<mail>/<complaint>")
def add_info(name, l_name, mail, complaint):
    connection = sqlite3.connect("complaints.db")
    try:
        cursor = connection.cursor()

        # Creating the table with columns for name, last_name, email, and complaint
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ComplaintDB (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                last_name TEXT,
                email TEXT,
                complaint TEXT
            )
        """)
        # Inserting values into the table
        cursor.execute("""
            INSERT INTO ComplaintDB (name, last_name, email, complaint) 
            VALUES (?, ?, ?, ?)
        """, (name, l_name, mail, complaint))

        # Commit changes
        connection.commit()
        print("Data added to the database.")

        return redirect(url_for("go_home"))
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return "An error occurred while accessing the database", 500
    finally:
        connection.close()

@app.route("/home")
def go_home():
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
