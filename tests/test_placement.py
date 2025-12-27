import pytest
from baip import Baip


def place1():
    b = Baip()
    placement = Baip.Placement(7, Baip.PieceType.KIT)
    c = b.apply_placement(placement)
    for y in range(c.len_y):
        for x in range(c.len_x):
            loc = c.index_to_loc(x, y)
            assert c.board[loc] == (
                Baip.Square.KIT_A if loc == placement.loc else Baip.Square.EMPTY
            )
