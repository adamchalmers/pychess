import piece
from utils import *
from board import Board
import threading
import move
import outcomes


class Game():
  
  def __init__(self, color, pw, game_id):
    self.game_id = game_id
    assert color in [WHITE, BLACK], "Invalid player"
    self.auth = {color: pw}
    self.board = Board()
    self.lock = threading.Lock()
    self.turns = 0
    self.winner = ""

  def pretty(self):
    src = self.pretty_no_borders()
    n = src.find("\n")
    header = "," + "="*26 + ".\n"
    out = header
    if self.board.turn == WHITE:
      color = "w"
    else:
      color = "b"
    out += ("|         " + self.game_id + " (%s)" % color).ljust(27) + "|\n"
    out += header.replace(".", "|").replace(",", "|")
    out += "|   0  1  2  3  4  5  6  7 |\n"
    out += "|%s|\n" % ("-"*26)
    for i, line in enumerate(src.split("\n")[1:-1]):
      out += "|%s| %s|\n" % (i, line)
    out += header.replace(".", "'").replace(",", "'")
    return out

  def pretty_no_borders(self):
    out = self.game_id
    all_pieces = self.board.all_pieces()
    if self.board.turn == WHITE:
      out += " (white)\n"
    else:
      out += " (black)\n"
    for i in range(8):
      for j in range(8):
        out += str(all_pieces[j][i]) + " "
      out = out[:-1] + "\n"
    out = out.replace("None", "..")
    return out

  def check_auth(self, color, pw):
    return color in self.auth and self.auth[color] == pw

  def add_player(self, color, pw):
    assert color not in self.auth, "player already added"
    assert color in [BLACK, WHITE], "invalid player"
    self.auth[color] = pw

  def move(self, move):
    """Executes the move encoded in a Move object on the current game.
       Raises IllegalMoveException if the move is illegal (fails validation)"""
    if self.board.turn != move.player:
      raise ActionNotAllowedException("It's not your turn!")
    if self.winner != "":
      raise ActionNotAllowedException("Game is over!")
    outcome = move.validate()

    # Handle special rules, like castling or promotion
    if outcome is not None:
      result = outcome[0]
      print outcome

      if result == outcomes.CASTLING:
        x1, y1, x2, y2 = outcome[1:]
        rook = move.board.at(x1,y1)
        assert type(rook) == piece.Rook
        rook.x = x2
        rook.y = y2

      elif result == outcomes.EN_PASSANTING:
        tx, ty = outcome[1:]
        pawn = move.board.at(tx, ty)
        assert type(pawn) == piece.Pawn
        move.board._pieces.remove(pawn)

      elif result == outcomes.PROMOTING:
        args = move.player, move.piece.x, move.piece.y
        new_piece = {
          "Q": piece.Queen(*args),
          "B": piece.Bishop(*args),
          "R": piece.Rook(*args),
          "N": piece.Knight(*args),
        }.get(move.promo)
        if new_piece is None:
          raise IllegalMoveException("You didn't choose a new piece to promote your pawn to!")
        self.board._pieces.remove(move.piece)
        self.board._pieces.add(new_piece)
        move.piece = new_piece
        
      else:
        raise Exception("Unexpected outcome %s" % str(outcome))

    # Execute the move.
    self.board.move(move.piece, move.x, move.y)
    self.board.turn = not self.board.turn
    move.piece.after_move()
    self.turns += 1

    # Check for checkmate
    if not self.board.moves_open(not move.piece.color):
      if self.board.checked(not move.piece.color):
        self.winner = {WHITE: "w", BLACK: "b"}[move.piece.color]
      else:
        self.winner = "s"

  def serialize(self):
    return {"board": self.serialize_board, 
        "turn": color_to_str(self.board.turn),
        "time": self.turns,
        "winner": self.winner,
      }

  @property
  def serialize_board(self):
    out = ""
    for row in self.board.all_pieces():
      for piece in row:
        if piece is None:
          out += ".."
        else:
          out += str(piece)
    return out
