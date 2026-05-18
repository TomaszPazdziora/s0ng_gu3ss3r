from flask import Flask, render_template, request, redirect, url_for
from server import Server
from player import Player
from flask_socketio import SocketIO, emit

app  = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app, cors_allowed_origins="*")

players = {}
scores = {}

# ============= SERVER ROUTES =============
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        role = request.form.get("role")
        if role == "server":
            server = Server()
            print(f"server: {server.name}")
        elif role == "player":
            print("new player created!")
            return render_template("user.html")
    return render_template("roles.html")

@app.route("/guess/<username>")
def guess(username):
    songs = ["song1", "song2", "song3"]
    return render_template("guess.html", songs=songs, username=username, score="420")

@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        print("create user path")
        username = request.form.get("username")
        return redirect(url_for("guess", username=username))
    return render_template("user.html")

# ============= SOCKETS ROUTES =============
@socketio.on("connect")
def handle_connect():
    print("CLIENT CONNECTED")

@socketio.on("disconnect")
def handle_connect():
    print("CLIENT DISCONNECTED")

@socketio.on("answer")
def handle_answer(data):
    username = players[request.sid]
    answer = data["answer"]
    print(f"user: {username}, answered: {answer}")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)