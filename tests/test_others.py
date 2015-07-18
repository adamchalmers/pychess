from chess import *
from chess.piece import King, Rook, Pawn, Bishop
from chess.board import Board
from nose.tools import assert_equals, assert_raises
import chess.outcomes

def test_copy():
  """Test piece copying."""
  king1 = King(WHITE, 0, 0)
  king2 = king1.copy()
  assert king1 is not king2
  assert king1.x == king2.x
  assert king1.y == king2.y
  assert king1.char == king2.char

def test_check_small():
  board = Board()
  king = King(BLACK, 0, 0)
  rook = Rook(WHITE, 2, 2)
  board._pieces = {king, rook}
  assert not board.checked(BLACK)
  board.move(rook, 2, 0)
  assert board.checked(BLACK)

def test_check_medium():
  board = Board()
  king = King(BLACK, 0, 0)
  rook = Rook(WHITE, 2, 2)
  pawn = Pawn(WHITE, 7, 3)
  bishop = Bishop(WHITE, 1, 3)
  enemy_king = King(WHITE, 6, 6)
  board._pieces = {king, rook, pawn, bishop, enemy_king}
  assert not board.checked(BLACK)
  board.move(rook, 2, 0)
  assert board.checked(BLACK)
  assert not board.checked(WHITE)

def test_copy():
  board = Board()
  king = King(BLACK, 0, 0)
  rook = Rook(WHITE, 2, 2)
  board._pieces = {king, rook}
  clone = board.copy()
  assert len(clone._pieces) == len(board._pieces)
  for piece in clone._pieces:
    assert piece not in board._pieces

def test_moves_tiny():
  board = Board()
  king = King(BLACK, 0, 0)
  r = Rook(WHITE, 4, 0)
  board._pieces = {king, r}
  assert_equals(board.moves_open(BLACK), True)

def test_checkmate():
  g = Game(WHITE, "pw", "adam1")
  bk = King(BLACK, 0, 0)
  wr1 = Rook(WHITE, 4, 0)
  wr2 = Rook(WHITE, 4, 4)
  wk = King(WHITE, 7, 7)
  g.board._pieces = {bk, wr1, wr2, wk}
  assert_equals(g.board.moves_open(BLACK), True)
  g.move(Move(4, 4, 4, 1, WHITE, g.board))
  assert_equals(g.winner, "w")
  with assert_raises(ActionNotAllowedException):
    g.move(Move(0, 0, 0, 1, BLACK, g.board))

def test_no_checkmate():
  g = Game(WHITE, "pw", "adam1")
  bk = King(BLACK, 0, 0)
  wk = King(WHITE, 7, 7)
  g.board._pieces = {bk, wk}
  assert g.winner == ""
  g.move(Move(7, 7, 7, 6, WHITE, g.board))
  assert g.winner == ""
  g.move(Move(0, 0, 0, 1, BLACK, g.board))
  assert g.winner == ""


def test_stalemate():
  g = Game(WHITE, "pw", "adam1")
  bk = King(BLACK, 0, 0)
  wr1 = Rook(WHITE, 1, 7)
  wr2 = Rook(WHITE, 7, 2)
  g.board._pieces = {bk, wr1, wr2}
  g.move(Move(7, 2, 7, 1, WHITE, g.board))
  assert_equals(g.winner, "s")
