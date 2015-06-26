from flask import jsonify

class ChessException(Exception):
    pass

WHITE = True
BLACK = False

def str_to_color(string):
    if string.lower() == "white":
        return WHITE
    elif string.lower() == "black":
        return BLACK
    raise ChessException("%s is not a valid color" % string)

def json_error(msg):
    return jsonify(error=msg)

def json_data(data):
    return jsonify(error="", data=data)

