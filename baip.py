from dataclasses import dataclass, field
from enum import Enum
import copy


class Baip:

    class Square(Enum):
        EMPTY = 0
        KIT_A = 1
        CAT_A = 2
        KIT_B = 3
        CAT_B = 4

        def to_char(self):
            if self is Baip.Square.EMPTY:
                return "."
            if self is Baip.Square.KIT_A:
                return "A"
            if self is Baip.Square.CAT_A:
                return "a"
            if self is Baip.Square.KIT_B:
                return "B"
            if self is Baip.Square.CAT_B:
                return "b"

        def is_empty(self):
            return self is Baip.Square.EMPTY

        def is_cat(self):
            return self in (Baip.Square.CAT_A, Baip.Square.CAT_B)

        def is_kit(self):
            return self in (Baip.Square.KIT_A, Baip.Square.KIT_B)

        def is_player(self, player):
            if player == 0:
                return self in (Baip.Square.CAT_A, Baip.Square.KIT_A)
            else:
                return self in (Baip.Square.CAT_B, Baip.Square.KIT_B)

    @dataclass()
    class Pieces:
        Cat: int = 8
        Kit: int = 0
        TotalKits: int = 0

        def has_cats(self):
            return self.Cat > 0

        def has_kits(self):
            return self.Kit > 0

    class PieceType(Enum):
        KIT = 0
        CAT = 1

    class Placement:
        loc: int
        piece: "Baip.PieceType"

        def __init__(self, loc, piece):
            self.loc = loc
            self.piece = piece

    def __init__(self, state=None):
        if state:
            self.board = state.board.copy()
            self.player = state.player
            self.pieces = copy.deepcopy(state.pieces)
        else:
            self.board = [Baip.Square.EMPTY for _ in range(self.len_x * self.len_y)]
            self.player = 0
            self.pieces = [Baip.Pieces(), Baip.Pieces()]

    def get_legal_removes(self):
        removes: list[int] = []
        player = self.player
        pieces = self.pieces[player]
        if not pieces.has_cats() and not pieces.has_kits():
            for loc, s in enumerate(self.board):
                if s.is_player(player):
                    removes.append(loc)
        return removes

    def get_legal_placements(self):
        placements: list[Baip.Placement] = []
        pieces = self.pieces[self.player]
        has_cats = pieces.has_cats()
        has_kits = pieces.has_kits()
        for loc, s in enumerate(self.board):
            if s.is_empty():
                if has_cats:
                    placements.append(Baip.Placement(loc, Baip.PieceType.CAT))
                if has_kits:
                    placements.append(Baip.Placement(loc, Baip.PieceType.KIT))
        return placements

    def apply_placement(self, placement):
        state = Baip(self)
        player = self.player
        state.player = 0 if state.player == 1 else 1
        if placement.piece == Baip.PieceType.CAT:
            state.pieces[player].Cat -= 1
            state.board[placement.loc] = (
                Baip.Square.CAT_A if player == 0 else Baip.Square.CAT_B
            )
        else:
            state.pieces[player].Kit -= 1
            state.board[placement.loc] = (
                Baip.Square.KIT_A if player == 0 else Baip.Square.KIT_B
            )
        return state

    def apply_remove(self, loc):
        state = Baip(self)
        player = self.player
        state.player = 0 if state.player == 1 else 1
        s = state.board[loc]
        state.pieces[player].Cat += s.is_cat()
        state.pieces[player].Kit += s.is_kit()
        state.board[loc] = Baip.Square.EMPTY
        return state

    def print_state(self):
        for y in range(self.len_y):
            for x in range(self.len_x):
                loc = x + y * self.len_x
                print(self.board[loc].to_char(), end="")
            if y == 0:
                print(f"  Player A:{" (current)" if self.player == 0 else ""}")
            if y == 1:
                print(f"    Cats    = {self.pieces[0].Cat}")
            if y == 2:
                print(f"    Kittens = {self.pieces[0].Kit}")
            if y == 3:
                print(f"  Player B:{" (current)" if self.player == 1 else ""}")
            if y == 4:
                print(f"    Cats    = {self.pieces[1].Cat}")
            if y == 5:
                print(f"    Kittens = {self.pieces[1].Kit}")

    len_x: int = 6
    len_y: int = 6
    board: list[Square]
    player: int
    pieces: list[Pieces]
