import pytest
from baip import Baip


def test_legal_promotions():
    b = Baip()
    promotions = b.get_legal_promotions()
    assert len(promotions) == 0

    b = Baip()
    b.board[b.index_to_loc(0, 0)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(1, 0)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(2, 0)] = Baip.Square.KIT_A
    promotions = b.get_legal_promotions()
    assert len(promotions) == 1
    assert promotions[0] == (0, 0, 1, 0)

    b = Baip()
    b.board[b.index_to_loc(0, 1)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(1, 0)] = Baip.Square.KIT_B
    b.board[b.index_to_loc(2, 0)] = Baip.Square.KIT_A
    promotions = b.get_legal_promotions()
    assert len(promotions) == 0

    b = Baip()
    b.board[b.index_to_loc(4, 2)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(4, 3)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(4, 4)] = Baip.Square.KIT_A
    promotions = b.get_legal_promotions()
    assert len(promotions) == 1
    assert promotions[0] == (4, 2, 0, 1)

    b = Baip()
    b.board[b.index_to_loc(3, 2)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(4, 2)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(5, 2)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(4, 3)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(3, 4)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(4, 4)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(5, 4)] = Baip.Square.KIT_A
    promotions = b.get_legal_promotions()
    assert len(promotions) == 5
    assert promotions[0] == (3, 2, 1, 1)
    assert promotions[1] == (3, 2, 1, 0)
    assert promotions[2] == (4, 2, 0, 1)
    assert promotions[3] == (5, 2, -1, 1)
    assert promotions[4] == (3, 4, 1, 0)

    b = Baip()
    b.board[b.index_to_loc(3, 2)] = Baip.Square.KIT_B
    b.board[b.index_to_loc(4, 2)] = Baip.Square.CAT_B
    b.board[b.index_to_loc(5, 2)] = Baip.Square.KIT_B
    b.board[b.index_to_loc(4, 3)] = Baip.Square.CAT_B
    b.board[b.index_to_loc(3, 4)] = Baip.Square.CAT_B
    b.board[b.index_to_loc(4, 4)] = Baip.Square.KIT_B
    b.board[b.index_to_loc(5, 4)] = Baip.Square.KIT_B
    promotions = b.get_legal_promotions()
    assert len(promotions) == 0
    b = b.next_turn()
    promotions = b.get_legal_promotions()
    assert len(promotions) == 5
    assert promotions[0] == (3, 2, 1, 1)
    assert promotions[1] == (3, 2, 1, 0)
    assert promotions[2] == (4, 2, 0, 1)
    assert promotions[3] == (5, 2, -1, 1)
    assert promotions[4] == (3, 4, 1, 0)


def test_promotions():
    b = Baip()
    promotions = b.get_legal_promotions()
    assert len(promotions) == 0

    b = Baip()
    b.board[b.index_to_loc(3, 2)] = Baip.Square.KIT_A
    b.board[b.index_to_loc(4, 2)] = Baip.Square.CAT_A
    b.board[b.index_to_loc(5, 2)] = Baip.Square.KIT_A
    b.pieces[0].TotalCats = 1
    b.pieces[0].Kit -= 2
    c = b.apply_promotion(3, 2, 1, 0)
    assert c.pieces[0].TotalCats == 3
    assert c.pieces[0].Cat == 3
    assert c.pieces[0].Kit == 6
    assert c.board[b.index_to_loc(3, 2)] == Baip.Square.EMPTY
    assert c.board[b.index_to_loc(4, 2)] == Baip.Square.EMPTY
    assert c.board[b.index_to_loc(5, 2)] == Baip.Square.EMPTY
