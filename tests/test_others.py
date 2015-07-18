from chess import *
from chess.piece import King, Rook, Pawn, Bishop
from chess.board import Board

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

