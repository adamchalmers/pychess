from utils import *
import validate


class Move():
  def __init__(self, x1, y1, x2, y2, player, game):
    self.player = player
    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2
    self.piece = str(game.board.at(x1, y1))

  def validate(self, game):
    validate.validate(self, game)

  def __str__(self):
    return "(%s,%s) (%s,%s) %s" % (self.y1, self.x1, self.y2, self.x2, self.piece)

