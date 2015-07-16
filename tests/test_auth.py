from chess import *
from nose.tools import assert_true, assert_equal, assert_raises

def test_auth():
  g = Game(WHITE, "adampw", "adamgame")
  print g.pretty()
  assert g.check_auth(WHITE, "adampw")
  assert not g.check_auth(WHITE, "wrong pw")

  g.add_player(BLACK, "black pw")
  assert g.check_auth(BLACK, "black pw")

  with assert_raises(AssertionError):
    g.add_player(BLACK, "black 2nd pw")
