import pytest
from baip import Baip


def test_terminal_cats():
    b = Baip()
    assert not b.is_terminal()
    assert not b.is_terminal(0)
    assert not b.is_terminal(1)
    b = b.next_turn()
    assert not b.is_terminal()
    assert not b.is_terminal(0)
    assert not b.is_terminal(1)
    b = b.next_turn()
    b.pieces[0].Cat = 8
    b.pieces[0].TotalCats = 8
    assert not b.is_terminal()
    assert not b.is_terminal(0)
    assert not b.is_terminal(1)
    b = b.next_turn()
    assert not b.is_terminal()
    assert not b.is_terminal(0)
    assert not b.is_terminal(1)
    b = b.next_turn()
    b.pieces[0].Cat = 0
    b.pieces[0].TotalCats = 8
    assert b.is_terminal()
    assert b.is_terminal(0)
    assert not b.is_terminal(1)
    b = b.next_turn()
    assert not b.is_terminal()
    assert b.is_terminal(0)
    assert not b.is_terminal(1)

    b = b.next_turn()
    b.pieces[1].Cat = 8
    b.pieces[1].TotalCats = 8
    assert b.is_terminal()
    assert b.is_terminal(0)
    assert not b.is_terminal(1)
    b = b.next_turn()
    assert not b.is_terminal()
    assert b.is_terminal(0)
    assert not b.is_terminal(1)
    b = b.next_turn()
    b.pieces[1].Cat = 0
    b.pieces[1].TotalCats = 8
    assert b.is_terminal()
    assert b.is_terminal(0)
    assert b.is_terminal(1)
    b = b.next_turn()
    assert b.is_terminal()
    assert b.is_terminal(0)
    assert b.is_terminal(1)


def test_terminal_row():
    b = Baip()
    assert not b.is_terminal()
    assert not b.is_terminal(0)
    assert not b.is_terminal(1)
    b = b.next_turn()
    # player 1
    assert not b.is_terminal()
    assert not b.is_terminal(0)
    assert not b.is_terminal(1)

    b = b.next_turn()
    # player 0
    b.board[b.index_to_loc(0, 0)] = Baip.Square.CAT_A
    assert not b.is_terminal()
    assert not b.is_terminal(0)
    assert not b.is_terminal(1)

    b.board[b.index_to_loc(1, 0)] = Baip.Square.CAT_A
    assert not b.is_terminal()
    assert not b.is_terminal(0)
    assert not b.is_terminal(1)

    # horizontal
    b.board[b.index_to_loc(2, 0)] = Baip.Square.CAT_A
    assert b.is_terminal()
    assert b.is_terminal(0)
    assert not b.is_terminal(1)
    b.board[b.index_to_loc(2, 0)] = Baip.Square.EMPTY

    b.board[b.index_to_loc(4, 2)] = Baip.Square.CAT_B
    assert not b.is_terminal()
    assert not b.is_terminal(0)
    assert not b.is_terminal(1)

    b.board[b.index_to_loc(4, 3)] = Baip.Square.CAT_B
    assert not b.is_terminal()
    assert not b.is_terminal(0)
    assert not b.is_terminal(1)

    b.board[b.index_to_loc(5, 4)] = Baip.Square.CAT_B
    assert not b.is_terminal()
    assert not b.is_terminal(0)
    assert not b.is_terminal(1)

    # vertical
    b.board[b.index_to_loc(4, 4)] = Baip.Square.CAT_B
    assert not b.is_terminal()
    assert not b.is_terminal(0)
    assert b.is_terminal(1)
    b.board[b.index_to_loc(4, 4)] = Baip.Square.EMPTY
    assert not b.is_terminal(1)

    b.board[b.index_to_loc(3, 2)] = Baip.Square.CAT_B
    assert not b.is_terminal()
    assert not b.is_terminal(0)
    assert b.is_terminal(1)
    b.board[b.index_to_loc(3, 2)] = Baip.Square.EMPTY
    assert not b.is_terminal(1)

    b.board[b.index_to_loc(5, 2)] = Baip.Square.CAT_B
    b.board[b.index_to_loc(3, 4)] = Baip.Square.CAT_B
    assert not b.is_terminal()
    assert not b.is_terminal(0)
    assert b.is_terminal(1)
    b.board[b.index_to_loc(5, 2)] = Baip.Square.EMPTY
    b.board[b.index_to_loc(3, 4)] = Baip.Square.EMPTY
    assert not b.is_terminal(1)
