from chess import *
from nose.tools import assert_true, assert_equal, assert_raises

def test_game_small():
  g = Game(WHITE, "pw", "game1")
  m1 = move.Move(0, 6, 0, 4, WHITE, g)
  g.move(m1)
  m2 = move.Move(1, 1, 1, 3, BLACK, g)
  g.move(m2)
  m3 = move.Move(5, 6, 5, 5, WHITE, g)
  g.move(m3)
  m4 = move.Move(1, 3, 0, 4, BLACK, g)
  g.move(m4)
  m5 = move.Move(0, 7, 0, 4, WHITE, g)
  g.move(m5)

def test_validation_core():
  g = Game(WHITE, "pw", "game1")
  # Can't move a piece onto another piece you own
  with assert_raises(MoveException): g.move(Move(0,7,0,6, WHITE, g))
  # Can't move an empty square
  with assert_raises(MoveException): g.move(Move(4,4,0,6, WHITE, g))
  # Can't move an opponent's piece
  with assert_raises(MoveException): g.move(Move(0,1,0,2, WHITE, g))
  # Can't move if it's not your turn
  with assert_raises(MoveException): g.move(Move(0,1,0,2, BLACK, g))
  # Can't move invalid coordinates
  with assert_raises(MoveException): g.move(Move(0,8,0,5, WHITE, g))
  with assert_raises(MoveException): g.move(Move(0,-1,0,5, WHITE, g))
  with assert_raises(MoveException): g.move(Move(8,6,0,5, WHITE, g))
  with assert_raises(MoveException): g.move(Move(-1,6,0,5, WHITE, g))
  with assert_raises(MoveException): g.move(Move(0,6,-8,5, WHITE, g))
  with assert_raises(MoveException): g.move(Move(0,6,17,5, WHITE, g))
  with assert_raises(MoveException): g.move(Move(0,6,0,9, WHITE, g))
  with assert_raises(MoveException): g.move(Move(0,6,0,-2, WHITE, g))
  # Can't move a non-player
  with assert_raises(MoveException): g.move(Move(0,1,0,2, 3003, g))

def test_validation_pawn():
  g = Game(WHITE, "pw", "game1")
  wp = g.board.at(0,6)
  bp = g.board.at(0,1)
  # Two pawns in front of each other should block movement and refuse attack.
  wp.x, wp.y = 4,4
  bp.x, bp.y = 4,3
  with assert_raises(MoveException): g.move(Move(4,4,4,3, WHITE, g))
  with assert_raises(MoveException): g.move(Move(4,4,3,3, WHITE, g))
  with assert_raises(MoveException): g.move(Move(4,4,5,3, WHITE, g))
  g.turn = BLACK
  with assert_raises(MoveException): g.move(Move(4,3,4,3, BLACK, g))
  with assert_raises(MoveException): g.move(Move(4,3,4,4, BLACK, g))
  with assert_raises(MoveException): g.move(Move(4,3,3,4, BLACK, g))
  with assert_raises(MoveException): g.move(Move(4,3,5,4, BLACK, g))
  # Pawns can move 2 squares from starting position
  g.move(Move(1,1,1,3, BLACK, g))
  g.move(Move(6,6,6,4, WHITE, g))
  # After, they can only move one square.
  with assert_raises(MoveException): g.move(Move(1,3,1,5, BLACK, g))
  g.move(Move(1,3,1,4, BLACK, g))
  with assert_raises(MoveException): g.move(Move(6,4,6,2, WHITE, g))
  g.move(Move(6,4,6,3, WHITE, g))

def test_en_passant():
  g = Game(WHITE, "pw", "game1")
  assert not g.board.at(3,6).en_passantable
  g.move(Move(3,6,3,4, WHITE, g))
  assert g.board.at(3,4).en_passantable
  g.move(Move(7,1,7,2, BLACK, g))
  g.move(Move(3,4,3,3, WHITE, g))
  g.move(Move(4,1,4,3, BLACK, g))
  assert g.board.at(4,3).en_passantable
  g.move(Move(3,3,4,2, WHITE, g))

def test_validation_bishop():
  g = Game(WHITE, "pw", "game1")
  wb = g.board.at(5, 7)
  assert wb.char == "B"
  # Bishop can't move at the start
  with assert_raises(MoveException): g.move(Move(5, 7, 4, 6, WHITE, g))
  with assert_raises(MoveException): g.move(Move(5, 7, 4, 8, WHITE, g))
  with assert_raises(MoveException): g.move(Move(5, 7, 6, 6, WHITE, g))
  with assert_raises(MoveException): g.move(Move(5, 7, 6, 8, WHITE, g))
  # Move the bishop along all four diagonals. 
  g.move(Move(4,6,4,5, WHITE, g))
  g.turn = WHITE
  g.move(Move(5,7,2,4, WHITE, g))
  g.turn = WHITE
  g.move(Move(2,4,1,3, WHITE, g))
  g.turn = WHITE
  g.move(Move(1,3,0,4, WHITE, g))
  g.turn = WHITE
  g.move(Move(0,4,1,5, WHITE, g))
  g.turn = WHITE
  g.move(Move(1,5,2,4, WHITE, g))
  # Can't move to 6,0
  g.turn = WHITE
  with assert_raises(MoveException): g.move(Move(2,4,6,0, WHITE, g))
  # Can move to 5,1
  g.move(Move(2,4,5,1, WHITE, g))

