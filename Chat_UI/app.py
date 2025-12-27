from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = "secret"
socketio = SocketIO(app)

def get_db():
    return sqlite3.connect("database.db")

# ---------- AUTH ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()

        if user and check_password_hash(user[3], password):
            session["user"] = user[1]
            return redirect("/chat")

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO users VALUES (NULL,?,?,?)",
                    (username, email, password))
        db.commit()

        return redirect("/")

    return render_template("signup.html")

@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect("/")
    return render_template("chat.html", user=session["user"])

# ---------- SOCKET ----------
@socketio.on("send_message")
def handle_message(data):
    emit("receive_message", data, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)
