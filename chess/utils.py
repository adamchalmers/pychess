from flask import jsonify

class ChessException(Exception):
    pass

class MoveException(ChessException):
  pass

WHITE = True
BLACK = False

def str_to_color(string):
    if string.lower() == "white":
        return WHITE
    elif string.lower() == "black":
        return BLACK
    raise ChessException("%s is not a valid color" % string)

def color_to_str(color):
    if color == WHITE:
        return "white"
    elif color == BLACK:
        return "black"
    raise ChessException("%s is not a valid color" % color)

def json_error(msg):
    return jsonify(error=msg)

def json_data(data):
    return jsonify(error="", data=data)


def path_clear(piece, board, dx, dy, dst_x, dst_y):
  """Checks if the path from m's start to m's end is clear."""
  x = piece.x + dx
  y = piece.y + dy
  while x < 8 and y < 8 and x >= 0 and y >= 0:
    if dst_x == x and dst_y == y:
      return
    if board.at(x,y) is not None:
      raise MoveException("There's a piece in your way.")
    x += dx
    y += dy
  raise MoveException("You can't reach that point.")