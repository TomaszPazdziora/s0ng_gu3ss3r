from flask import Flask, render_template, request, redirect, url_for
from server import Server
from player import Player
from flask_socketio import SocketIO, emit
from random import randint
import time

app  = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app, cors_allowed_origins="*")

server = Server()
rand_songs = ['a', 'v', 'b', 'c', 'f', 'k', 'l', 'p']

# ============= SERVER ROUTES =============
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        role = request.form.get("role")
        if role == "server":
            return redirect(url_for("scoreboard"))
        elif role == "player":
            return redirect(url_for("create_user"))
    return render_template("roles.html")

@app.route("/scoreboard")
def scoreboard():
    global server
    return render_template(
        "scoreboard.html",
        players=server.players
    )

@app.route("/game/<username>")
def game(username):
    return render_template("game.html", username=username, score="420")

@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    global server
    if request.method == "POST":
        print("user added")
        server.active = True
        username = request.form.get("username")
        server.players.append(Player(username))
        print(f"player name: {username}")
        return redirect(url_for("game", username=username))
    return render_template("user.html")

# ============= SOCKETS ROUTES =============
@socketio.on("connect")
def handle_connect():
    print("CLIENT CONNECTED")

@socketio.on("disconnect")
def handle_connect():
    print("CLIENT DISCONNECTED")

def draw_songs():
    global server
    while True:
        if server.active:
            songs_set = [rand_songs[randint(0, len(rand_songs)-1)] for _ in range(3)]
            socketio.emit("new_songs", {
                "songs": songs_set
            })
        socketio.sleep(3)

if __name__ == "__main__":
    socketio.start_background_task(draw_songs)
    socketio.run(app, host="0.0.0.0", port=5000)