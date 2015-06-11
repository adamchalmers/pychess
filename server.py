from flask import Flask, render_template, request, redirect, url_for
from chess import Game
from utils import *
app = Flask(__name__)
games = {"adam1": Game(WHITE, "password", "adam1")}

class ChessServerError(Exception):
	pass

@app.route("/game/<game_id>")
def game(game_id):
	if game_id in games:
		return render_template("game.html", game_id=game_id)
	else:
		return render_template("no_game.html", games=games)

@app.route("/new.html")
def new_game():
	return render_template("new.html")

@app.route("/")
def index():
	return render_template("index.html", games=games)

@app.route("/auth", methods=["POST"])
def auth():
	print "Handling auth..."
	if request.form["color"] == "white":
		color = WHITE
	elif request.form["color"] == "black":
		color = BLACK
	else:
		raise ChessServerError("%s is an invalid color" % request.form["color"])
	pw = request.form["pw"]
	game_id = request.form["game_id"]

	if game_id in games and games[game_id].auth[color] == pw:
		msg = "TRUE"
		print msg
		return msg
	else:
		msg = "FALSE"
		print msg
		return msg

if __name__ == "__main__":
	app.run(debug=True)
