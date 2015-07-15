from utils import *

class Move():
  def __init__(self, srcx, srcy, dstx, dsty, player, game):
    self.player = player
    self.piece = game.board.at(srcx, srcy)
    self.x = dstx
    self.y = dsty
    self.game = game
    self._str = "%s at (%s,%s) to (%s,%s)" % (str(self.piece), srcx, srcy, dstx, dsty)

  def validate(self):
    try:
      self._general_validation()

      # Validate piece-specific rules
      if self.game.board.at(self.x, self.y) is None:
        self.piece.can_move(self.game, self.x, self.y)
      else:
        self.piece.can_attack(self.game, self.x, self.y)

    except AssertionError as e:
      raise MoveException(str(e))

  def __str__(self):
    return self._str

  def _general_validation(self):
    # Basic rules of chess
    for i in [self.piece.x, self.piece.y, self.x, self.y]:
      assert i >= 0 and i < 8, "Invalid coordinate (%s)." % i
    assert self.game.turn == self.player, "It's not your turn."
    assert self.player in [BLACK, WHITE], "Invalid player."
    dst = self.game.board.at(self.x, self.y)
    assert dst is None or dst.color != self.player, "You can't move a piece onto another of your pieces."
    assert self.piece is not None, "The square you're trying to move doesn't have a piece."
    assert self.piece.color == self.player, "You can't move the opponent's pieces."
