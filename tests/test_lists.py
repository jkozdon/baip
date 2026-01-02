import pytest
from baip import Baip


def test_valid_empty_board():
    b = Baip()
    # ......  Player A: (current)
    # ......    Kittens = 8
    # ......    Cats    = 0
    # ......  Player B:
    # ......    Kittens = 8
    # ......    Cats    = 0
    placements = b.get_legal_placements()
    for loc in range(b.len_x * b.len_y):
        x, y = b.loc_to_index(loc)
        assert placements[loc] == Baip.Placement(x, y, Baip.PieceType.KIT)

    b.player = 1
    # ......  Player A:
    # ......    Kittens = 8
    # ......    Cats    = 0
    # ......  Player B: (current)
    # ......    Kittens = 8
    # ......    Cats    = 0
    placements = b.get_legal_placements()
    for loc in range(b.len_x * b.len_y):
        x, y = b.loc_to_index(loc)
        assert placements[loc] == Baip.Placement(x, y, Baip.PieceType.KIT)

    b.player = 0
    b.pieces[0].Cat = 1
    # ......  Player A: (current)
    # ......    Kittens = 8
    # ......    Cats    = 1
    # ......  Player B:
    # ......    Kittens = 8
    # ......    Cats    = 0
    placements = b.get_legal_placements()
    i = 0
    for loc in range(b.len_x * b.len_y):
        x, y = b.loc_to_index(loc)
        assert placements[i] == Baip.Placement(x, y, Baip.PieceType.KIT)
        i += 1
        assert placements[i] == Baip.Placement(x, y, Baip.PieceType.CAT)
        i += 1

    b.player = 1
    b.pieces[1].Cat = 1
    # ......  Player A:
    # ......    Kittens = 8
    # ......    Cats    = 1
    # ......  Player B:
    # ......    Kittens = 8
    # ......    Cats    = 1 (current)
    placements = b.get_legal_placements()
    i = 0
    for loc in range(b.len_x * b.len_y):
        x, y = b.loc_to_index(loc)
        assert placements[i] == Baip.Placement(x, y, Baip.PieceType.KIT)
        i += 1
        assert placements[i] == Baip.Placement(x, y, Baip.PieceType.CAT)
        i += 1

    b.player = 0
    b.pieces[0].Cat = 1
    b.pieces[0].Kit = 0
    # ......  Player A: (current)
    # ......    Kittens = 0
    # ......    Cats    = 1
    # ......  Player B:
    # ......    Kittens = 8
    # ......    Cats    = 0
    placements = b.get_legal_placements()
    i = 0
    for loc in range(b.len_x * b.len_y):
        x, y = b.loc_to_index(loc)
        assert placements[i] == Baip.Placement(x, y, Baip.PieceType.CAT)
        i += 1

    b.player = 1
    b.pieces[1].Cat = 1
    b.pieces[1].Kit = 0
    # ......  Player A:
    # ......    Kittens = 0
    # ......    Cats    = 1
    # ......  Player B: (current)
    # ......    Kittens = 0
    # ......    Cats    = 0
    placements = b.get_legal_placements()
    i = 0
    for loc in range(b.len_x * b.len_y):
        x, y = b.loc_to_index(loc)
        assert placements[i] == Baip.Placement(x, y, Baip.PieceType.CAT)
        i += 1


def test_valid_partial_filled():
    b = Baip()
    b.board[b.index_to_loc(0, 0)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(0, 1)] = Baip.Square.KIT_B
    b.board[b.index_to_loc(0, 4)] = Baip.Square.CAT_A
    b.board[b.index_to_loc(1, 2)] = Baip.Square.KIT_B
    b.board[b.index_to_loc(2, 2)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(2, 4)] = Baip.Square.KIT_B
    b.board[b.index_to_loc(3, 0)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(3, 2)] = Baip.Square.CAT_A
    b.board[b.index_to_loc(3, 4)] = Baip.Square.KIT_B
    b.board[b.index_to_loc(4, 2)] = Baip.Square.CAT_B
    b.board[b.index_to_loc(5, 1)] = Baip.Square.KIT_B
    b.board[b.index_to_loc(5, 5)] = Baip.Square.CAT_B
    # a..a..  Player A: (current)
    # b....b    Kittens = 8
    # .baAB.    Cats    = 0
    # ......  Player B:
    # A.bb..    Kittens = 8
    # .....B    Cats    = 0

    indices = [
        1,
        2,
        4,
        5,
        7,
        8,
        9,
        10,
        12,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        25,
        28,
        29,
        30,
        31,
        32,
        33,
        34,
        35,
    ]

    placements = b.get_legal_placements()
    for ind, placement in enumerate(placements):
        x, y = b.loc_to_index(indices[ind])
        assert placement == Baip.Placement(x, y, Baip.PieceType.KIT)

    b.pieces[0].Cat = 1
    placements = b.get_legal_placements()
    for ind, placement in enumerate(placements):
        x, y = b.loc_to_index(indices[ind // 2])
        assert placement == Baip.Placement(
            x,
            y,
            Baip.PieceType.KIT if ind % 2 == 0 else Baip.PieceType.CAT,
        )

    b.player = 1
    placements = b.get_legal_placements()
    for ind, placement in enumerate(placements):
        x, y = b.loc_to_index(indices[ind])
        assert placement == Baip.Placement(x, y, Baip.PieceType.KIT)

    b.pieces[1].Cat = 1
    placements = b.get_legal_placements()
    for ind, placement in enumerate(placements):
        x, y = b.loc_to_index(indices[ind // 2])
        assert placement == Baip.Placement(
            x,
            y,
            Baip.PieceType.KIT if ind % 2 == 0 else Baip.PieceType.CAT,
        )


def test_removes():
    b = Baip()
    b.board[b.index_to_loc(0, 0)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(3, 0)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(0, 1)] = Baip.Square.KIT_B
    b.board[b.index_to_loc(5, 1)] = Baip.Square.KIT_B
    b.board[b.index_to_loc(1, 2)] = Baip.Square.KIT_B
    b.board[b.index_to_loc(2, 2)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(3, 2)] = Baip.Square.CAT_A
    b.board[b.index_to_loc(4, 2)] = Baip.Square.CAT_B
    b.board[b.index_to_loc(0, 4)] = Baip.Square.CAT_A
    b.board[b.index_to_loc(2, 4)] = Baip.Square.KIT_B
    b.board[b.index_to_loc(3, 4)] = Baip.Square.KIT_B
    b.board[b.index_to_loc(5, 5)] = Baip.Square.CAT_B
    b.pieces[0].Kit = 0
    b.pieces[0].Cat = 0
    b.pieces[1].Kit = 4
    b.pieces[1].Cat = 4

    placements = b.get_legal_placements()
    assert len(placements) == 0

    removes = b.get_legal_removes()
    assert removes[0] == b.index_to_loc(0, 0)
    assert removes[1] == b.index_to_loc(3, 0)
    assert removes[2] == b.index_to_loc(2, 2)
    assert removes[3] == b.index_to_loc(3, 2)
    assert removes[4] == b.index_to_loc(0, 4)

    b.player = 1
    b.pieces[0].Kit = 4
    b.pieces[0].Cat = 4
    b.pieces[1].Kit = 0
    b.pieces[1].Cat = 0

    placements = b.get_legal_placements()
    assert len(placements) == 0

    removes = b.get_legal_removes()
    assert removes[0] == b.index_to_loc(0, 1)
    assert removes[1] == b.index_to_loc(5, 1)
    assert removes[2] == b.index_to_loc(1, 2)
    assert removes[3] == b.index_to_loc(4, 2)
    assert removes[4] == b.index_to_loc(2, 4)
    assert removes[5] == b.index_to_loc(3, 4)
    assert removes[6] == b.index_to_loc(5, 5)
