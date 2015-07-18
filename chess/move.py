from utils import *
import piece

class Move():
  def __init__(self, srcx, srcy, dstx, dsty, player, game, promo=None):
    self.player = player
    self.piece = game.board.at(srcx, srcy)
    self.x = dstx
    self.y = dsty
    self.game = game
    # Should be in (Q,N,B,R) and is the piece created if this move involves promotion
    self.promo = promo
    self._str = "%s at (%s,%s) to (%s,%s)" % (str(self.piece), srcx, srcy, dstx, dsty)

  def validate(self):
    try:
      self._general_validation()

      # Validate piece-specific rules
      if self.game.board.at(self.x, self.y) is None:
        outcome = self.piece.can_move(self.game.board, self.x, self.y)
      else:
        outcome = self.piece.can_attack(self.game.board, self.x, self.y)

      # Validate that the move won't leave the player in check.
      future = self.game.board.copy()
      future.move(future.at(self.piece.x, self.piece.y), self.x, self.y)
      assert not future.checked(self.player), "This move would leave you in check."

      # Have you checkmated your opponent?
      if future.num_moves(not self.player) == 0:
        if future.checked(not self.player):
          return piece.CHECKMATE
        else:
          return piece.STALEMATE

      return outcome

    except AssertionError as e:
      raise MoveException(str(e))

  def __str__(self):
    return self._str

  def _general_validation(self):
    """Generic moves of chess. Raises exceptions if move is illegal."""
    assert self.piece is not None, "There's no piece at this square."
    for i in [self.piece.x, self.piece.y, self.x, self.y]:
      assert i >= 0 and i < 8, "Invalid coordinate (%s)." % i
    assert self.game.turn == self.player, "It's not your turn."
    assert self.player in [BLACK, WHITE], "Invalid player."
    dst = self.game.board.at(self.x, self.y)
    assert dst is None or dst.color != self.player, "You can't move a piece onto another of your pieces."
    assert self.piece.color == self.player, "You can't move the opponent's pieces."
