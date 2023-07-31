from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ayushmp',
    'database': 'jitdb',
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Sample username and password (replace with your actual credentials)
valid_username = "user"
valid_password = "password"

@app.route("/", methods=["GET","POST"])
def login():
    error=None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == valid_username and password == valid_password:
            # Redirect to a success page or dashboard if credentials are correct
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password. Please try again."
    return render_template("login.html", error=error)

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    cursor.execute('SELECT * FROM jitdb.student')
    students = cursor.fetchall()
    return render_template("dashboard.html",students=students)

# Add student to the database
@app.route('/add', methods=['POST'])
def add_student():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        usn = request.form['usn']
        branch = request.form['semester']

        # Insert the new student record into the 'student' table
        cursor.execute('INSERT INTO student (id, name, usn, branch) VALUES (%s, %s, %s, %s)',
                       (id, name, usn, branch))
        conn.commit()

    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run(debug=True)
