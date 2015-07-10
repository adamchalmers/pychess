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

