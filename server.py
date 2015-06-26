from flask import Flask, render_template, request, redirect, url_for, jsonify
from chess import Game, Move, MoveException
from utils import *
app = Flask(__name__)
games = {"adam1": Game(WHITE, "password", "adam1")}

class ChessServerError(ChessException):
	pass

#############################
#           Pages           #
#############################

@app.route("/game/<game_id>")
def game(game_id):
	"""Renders HTML for the given game."""
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


#############################
#            API            #
#############################

@app.route("/state/<game_id>")
def state(game_id):
	"""Returns game state in JSON."""
	if game_id in games:
		with games[game_id].lock:
			data = games[game_id].serialize()
			return json_data(data=data)
	return json_error("no such game")

@app.route("/move/<game_id>/<player>/<int:x1>/<int:y1>/<int:x2>/<int:y2>")
def move(game_id, player, x1, y1, x2, y2):
	"""Receives and validates a move from the user."""

	if game_id not in games:
		return json_error("No such game!")
	player = str_to_color(player)
	move = Move(x1, y1, x2, y2, player, game_id)
	try:
		move.validate(games[game_id])
	except MoveException as e:
		return json_error(str(e))
	games[game_id].move(move)
	return state(game_id)


@app.route("/auth", methods=["POST"])
def auth():
	print "Handling auth..."
	color = str_to_color(request.form["color"])
	pw = request.form["pw"]
	game_id = request.form["game_id"]

	if game_id in games and games[game_id].auth[color] == pw:
		return json_error("")
	else:
		return json_error("wrong auth!")

if __name__ == "__main__":
	app.run(debug=True)
