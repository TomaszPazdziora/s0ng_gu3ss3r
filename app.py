from flask import Flask, render_template

songs = ["song1", "song2", "song3"]
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("roles.html")

@app.route("/guess")
def guess():
    return render_template("guess.html", songs=songs, username="norbi", score="420")

app.run(debug=True)