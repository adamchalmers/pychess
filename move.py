from utils import *
import validate


class Move():
  def __init__(self, srcx, srcy, dstx, dsty, player, game):
    self.player = player
    self.piece = game.board.at(srcx, srcy)
    self.x = dstx
    self.y = dsty
    self.game = game
    self._str = "%s at (%s,%s) to (%s,%s)" % (str(self.piece), srcx, srcy, dstx, dsty)

  def validate(self):
    validate.validate(self, self.game)

  def __str__(self):
    return self._str

