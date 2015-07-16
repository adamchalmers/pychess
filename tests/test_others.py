from chess import *
from chess.piece import King

def test_copy():
  """Test piece copying."""
  king1 = King(WHITE, 0, 0)
  king2 = king1.copy()
  assert king1 is not king2
  assert king1.x == king2.x
  assert king1.y == king2.y
  assert king1.char == king2.char