from flask import Flask, render_template, request, redirect, url_for, jsonify, request
from chess import *
import logging
app = Flask(__name__)
games = {}

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

@app.route("/new/<game_id>")
def new_game(game_id):
  if game_id in games:
    return json_error("game already exists.")
  games[game_id] = Game()
  return json_error("")

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

  # Make the query string into a k/v dictionary.
  query = {}
  try:
    for kv in request.url[request.url.find("?")+1:].split("&"):
      k, v = kv.split("=")
      query[k] = v
  except ValueError:
    pass

  if game_id not in games:
    return json_error("No such game!")

  player = str_to_color(player)
  try:
    move = Move(x1, y1, x2, y2, player, games[game_id].board, promo=query.get("promo"))
    games[game_id].move(move)
  except ChessException as e:
    return json_error(str(e))

  return state(game_id)


@app.route("/auth", methods=["POST"])
def auth():
  print "Handling auth..."
  color = str_to_color(request.form["color"])
  pw = request.form["pw"]
  game_id = request.form["game_id"]

  if game_id not in games:
    return json_error("No such game ID!")

  # Right now, if they log into a player who hasn't played yet,
  # just set the password they send as that player's pass and log them in.
  if color not in games[game_id].auth:
    #games[game_id].auth[color] = pw
    return json_error("new auth")

  if games[game_id].auth[color] == pw:
    return json_data(request.form["color"])
  else:
    return json_error("wrong auth!")

@app.route("/new_auth", methods=["POST"])
def new_auth():
  print "Adding new auth"
  color = str_to_color(request.form["color"])
  pw = request.form["pw"]
  game_id = request.form["game_id"]

  if game_id not in games:
    return json_error("No such game ID!")

  if color in games[game_id].auth:
    return json_error("%s already has a password!" % color)

  games[game_id].auth[color] = pw
  return json_data(request.form["color"])


#############################
#            Misc           #
#############################

@app.route("/shutdown")
def shutdown():
  func = request.environ.get('werkzeug.server.shutdown')
  if func is None:
    raise RuntimeError('Not running with the Werkzeug Server')
  func()
  return 'Server shutting down...'

@app.route("/restart")
def restart():
  shutdown()
  app.run(debug=True)
  return redirect(url_for('/'))

def starting_games():
  games = {
    "adam1": Game(WHITE, "pw"),
    "endgame": Game(WHITE, "pw"),
  }
  games["endgame"].board._pieces = {
    piece.King(WHITE, 4, 6), 
    piece.King(BLACK, 7, 1),
    piece.Rook(WHITE, 0, 2),
    piece.Rook(WHITE, 6, 7),
  }
  return games

if __name__ == "__main__":
  log = logging.getLogger('werkzeug')
  #log.setLevel(logging.ERROR)
  games = starting_games()
  app.run(debug=True)
