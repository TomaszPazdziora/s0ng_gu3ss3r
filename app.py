from flask import Flask, render_template, request
from server import Server
from player import Player

songs = ["song1", "song2", "song3"]
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        role = request.form.get("role")
        if role == "server":
            server = Server()
            print(f"server: {server.name}")
        elif role == "player":
            print("new player created!") 
    return render_template("roles.html")

@app.route("/guess")
def guess():
    return render_template("guess.html", songs=songs, username="norbi", score="420")

app.run(debug=True)