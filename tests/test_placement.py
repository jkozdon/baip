import pytest
from baip import Baip


def test_kitten_placement():
    b = Baip()
    # ......  Player A: (current)
    # ......    Kittens = 8
    # ......    Cats    = 0
    # ......  Player B:
    # ......    Kittens = 8
    # ......    Cats    = 0
    assert b.player == 0
    assert b.pieces[0].Cat == 0
    assert b.pieces[0].Kit == 8
    assert b.pieces[1].Cat == 0
    assert b.pieces[1].Kit == 8
    for y in range(b.len_y):
        for x in range(b.len_x):
            loc = b.index_to_loc(x, y)
            b.board[loc] == Baip.Square.EMPTY

    place = Baip.Placement(b.index_to_loc(0, 0), Baip.PieceType.KIT)
    b = b.apply_placement(place)
    # a.....  Player A:
    # ......    Kittens = 7
    # ......    Cats    = 0
    # ......  Player B: (current)
    # ......    Kittens = 8
    # ......    Cats    = 0
    assert b.player == 1
    assert b.pieces[0].Cat == 0
    assert b.pieces[0].Kit == 7
    assert b.pieces[1].Cat == 0
    assert b.pieces[1].Kit == 8
    for y in range(b.len_y):
        for x in range(b.len_x):
            loc = b.index_to_loc(x, y)
            if x == 0 and y == 0:
                assert b.board[loc] == Baip.Square.KIT_A
            else:
                assert b.board[loc] == Baip.Square.EMPTY

    place = Baip.Placement(b.index_to_loc(2, 2), Baip.PieceType.KIT)
    # a.....  Player A: (current)
    # ......    Kittens = 7
    # .b....    Cats    = 0
    # ......  Player B:
    # ......    Kittens = 7
    # ......    Cats    = 0
    b = b.apply_placement(place)
    assert b.player == 0
    assert b.pieces[0].Cat == 0
    assert b.pieces[0].Kit == 7
    assert b.pieces[1].Cat == 0
    assert b.pieces[1].Kit == 7
    for y in range(b.len_y):
        for x in range(b.len_x):
            loc = b.index_to_loc(x, y)
            if x == 0 and y == 0:
                assert b.board[loc] == Baip.Square.KIT_A
            elif x == 2 and y == 2:
                assert b.board[loc] == Baip.Square.KIT_B
            else:
                assert b.board[loc] == Baip.Square.EMPTY

    place = Baip.Placement(b.index_to_loc(1, 1), Baip.PieceType.KIT)
    b = b.apply_placement(place)
    # ......  Player A:
    # .a....    Kittens = 7
    # ......    Cats    = 0
    # ...b..  Player B: (current)
    # ......    Kittens = 7
    # ......    Cats    = 0
    assert b.player == 1
    assert b.pieces[0].Cat == 0
    assert b.pieces[0].Kit == 7
    assert b.pieces[1].Cat == 0
    assert b.pieces[1].Kit == 7
    for y in range(b.len_y):
        for x in range(b.len_x):
            loc = b.index_to_loc(x, y)
            if x == 1 and y == 1:
                assert b.board[loc] == Baip.Square.KIT_A
            elif x == 3 and y == 3:
                assert b.board[loc] == Baip.Square.KIT_B
            else:
                assert b.board[loc] == Baip.Square.EMPTY

    place = Baip.Placement(b.index_to_loc(1, 3), Baip.PieceType.KIT)
    b = b.apply_placement(place)
    # ......  Player A: (current)
    # .a....    Kittens = 7
    # ......    Cats    = 0
    # .b.b..  Player B:
    # ......    Kittens = 6
    # ......    Cats    = 0
    assert b.player == 0
    assert b.pieces[0].Cat == 0
    assert b.pieces[0].Kit == 7
    assert b.pieces[1].Cat == 0
    assert b.pieces[1].Kit == 6
    for y in range(b.len_y):
        for x in range(b.len_x):
            loc = b.index_to_loc(x, y)
            if x == 1 and y == 1:
                assert b.board[loc] == Baip.Square.KIT_A
            elif x == 3 and y == 3:
                assert b.board[loc] == Baip.Square.KIT_B
            elif x == 1 and y == 3:
                assert b.board[loc] == Baip.Square.KIT_B
            else:
                assert b.board[loc] == Baip.Square.EMPTY

    place = Baip.Placement(b.index_to_loc(2, 4), Baip.PieceType.KIT)
    b = b.apply_placement(place)
    # ......  Player A:
    # .a....    Kittens = 6
    # b...b.    Cats    = 0
    # ......  Player B: (current)
    # ..a...    Kittens = 6
    # ......    Cats    = 0
    assert b.player == 1
    assert b.pieces[0].Cat == 0
    assert b.pieces[0].Kit == 6
    assert b.pieces[1].Cat == 0
    assert b.pieces[1].Kit == 6
    for y in range(b.len_y):
        for x in range(b.len_x):
            loc = b.index_to_loc(x, y)
            if x == 1 and y == 1:
                assert b.board[loc] == Baip.Square.KIT_A
            elif x == 4 and y == 2:
                assert b.board[loc] == Baip.Square.KIT_B
            elif x == 0 and y == 2:
                assert b.board[loc] == Baip.Square.KIT_B
            elif x == 2 and y == 4:
                assert b.board[loc] == Baip.Square.KIT_A
            else:
                assert b.board[loc] == Baip.Square.EMPTY

    place = Baip.Placement(b.index_to_loc(2, 0), Baip.PieceType.KIT)
    b = b.apply_placement(place)
    # ..b...  Player A: (current)
    # .a....    Kittens = 6
    # b...b.    Cats    = 0
    # ......  Player B:
    # ..a...    Kittens = 5
    # ......    Cats    = 0
    assert b.player == 0
    assert b.pieces[0].Cat == 0
    assert b.pieces[0].Kit == 6
    assert b.pieces[1].Cat == 0
    assert b.pieces[1].Kit == 5
    for y in range(b.len_y):
        for x in range(b.len_x):
            loc = b.index_to_loc(x, y)
            if x == 1 and y == 1:
                assert b.board[loc] == Baip.Square.KIT_A
            elif x == 4 and y == 2:
                assert b.board[loc] == Baip.Square.KIT_B
            elif x == 0 and y == 2:
                assert b.board[loc] == Baip.Square.KIT_B
            elif x == 2 and y == 4:
                assert b.board[loc] == Baip.Square.KIT_A
            elif x == 2 and y == 0:
                assert b.board[loc] == Baip.Square.KIT_B
            else:
                assert b.board[loc] == Baip.Square.EMPTY
