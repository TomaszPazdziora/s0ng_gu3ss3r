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
        username = request.form.get("username")
        server.players.append(Player(username))
        return redirect(url_for("game", username=username))
    return render_template("user.html")

@app.route("/activate_server", methods=["GET", "POST"])
def activate_server():
    global server
    if request.method == "POST":
        if server.paused is True:
            server.resume_round()
        elif server.active is False:
            server.activate_server()
    return redirect(url_for("scoreboard"))

@app.route("/skip_song", methods=["GET", "POST"])
def skip_song():
    global server
    if request.method == "POST":
        server.reset_round(socketio)
    return redirect(url_for("scoreboard"))

@app.route("/pause", methods=["GET", "POST"])
def pause():
    global server
    if request.method == "POST":
        server.pause_round()
    return redirect(url_for("scoreboard"))


# ============= SOCKETS ROUTES =============
@socketio.on("answer")
def handle_answer(data):
    global server
    if server.active and server.paused is False:
        username = data["username"]
        answer = data["answer"]

        print(f"{username} answered {answer}")
        server.validate_answer(username, answer)


def game_loop():
    global server

    while True:
        if server.active and server.paused is False:
            if server.round_active is False or server.is_round_time_elapsed():
                server.reset_round(socketio)
        socketio.sleep(0.5)

if __name__ == "__main__":
    socketio.start_background_task(game_loop)
    socketio.run(app, host="0.0.0.0", port=5000)