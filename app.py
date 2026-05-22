from flask import Flask, render_template, request, redirect, url_for
from server import Server
from player import Player
from flask_socketio import SocketIO, emit

app  = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

socketio = SocketIO(app, cors_allowed_origins="*")

server = Server()

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
        server.active = True
        username = request.form.get("username")
        server.players.append(Player(username))
        return redirect(url_for("game", username=username))
    return render_template("user.html")

# ============= SOCKETS ROUTES =============
@socketio.on("answer")
def handle_answer(data):
    global server

    username = data["username"]
    answer = data["answer"]

    print(f"{username} answered {answer}")
    server.validate_answer(username, answer)


def draw_songs():
    global server

    while True:
        if server.active:
            if server.round_active is False or server.is_round_time_elapsed():
                server.load_songs()
                socketio.emit("new_songs", {
                    "songs": server.songs_set
                })
        socketio.sleep(0.5)

if __name__ == "__main__":
    socketio.start_background_task(draw_songs)
    socketio.run(app, host="0.0.0.0", port=5000)