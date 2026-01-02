# TODO: Promotions
#       - three cats / kittens in a row
#       - Possible choice for resolution
# TODO: [optional] Add ability to check if move is valid

from dataclasses import dataclass
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
                return "a"
            if self is Baip.Square.CAT_A:
                return "A"
            if self is Baip.Square.KIT_B:
                return "b"
            if self is Baip.Square.CAT_B:
                return "B"

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
        Kit: int = 8
        Cat: int = 0
        TotalCats: int = 0

        def has_cats(self):
            return self.Cat > 0

        def has_kits(self):
            return self.Kit > 0

    class PieceType(Enum):
        KIT = 0
        CAT = 1

    class Placement:
        x: int
        y: int
        piece: "Baip.PieceType"

        def __init__(self, loc, piece):
            self.x = loc % 6
            self.y = loc // 6
            self.piece = piece

        def __eq__(self, other):
            return self.x == other.x and self.y == other.y and self.piece == other.piece

    def __init__(self, state=None):
        if state:
            self.board = state.board.copy()
            self.player = state.player
            self.pieces = copy.deepcopy(state.pieces)
        else:
            self.board = [Baip.Square.EMPTY for _ in range(self.len_x * self.len_y)]
            self.player = 0
            self.pieces = [Baip.Pieces(), Baip.Pieces()]

    def get_legal_promotions(self):
        promotions = []
        player = self.player
        len_x = self.len_x
        len_y = self.len_x

        def check(x, y, dx, dy):
            for i in range(3):
                nx = x + i * dx
                ny = y + i * dy
                if nx >= len_x or ny >= len_y:
                    return False
                loc = self.index_to_loc(nx, ny)
                if not self.board[loc].is_player(player):
                    return False
            return True

        dirs = [(0, 1), (1, 1), (1, 0), (-1, 1)]
        for y in range(len_y):
            for x in range(len_x):
                for dir in dirs:
                    if check(x, y, dir[0], dir[1]):
                        promotions.append((x, y, dir[0], dir[1]))
        return promotions

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
                if has_kits:
                    placements.append(Baip.Placement(loc, Baip.PieceType.KIT))
                if has_cats:
                    placements.append(Baip.Placement(loc, Baip.PieceType.CAT))
        return placements

    def loc_to_index(self, loc):
        x = loc % self.len_x
        y = loc // self.len_x
        return (x, y)

    def index_to_loc(self, x, y):
        return x + y * self.len_x

    def valid_index(self, x, y):
        return x >= 0 and x < self.len_x and y >= 0 and y < self.len_y

    def apply_placement(self, placement):
        state = Baip(self)
        player = self.player
        x, y = placement.x, placement.y
        loc = self.index_to_loc(x, y)
        if placement.piece == Baip.PieceType.CAT:
            state.pieces[player].Cat -= 1
            state.board[loc] = Baip.Square.CAT_A if player == 0 else Baip.Square.CAT_B
        else:
            state.pieces[player].Kit -= 1
            state.board[loc] = Baip.Square.KIT_A if player == 0 else Baip.Square.KIT_B
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx != 0 or dy != 0:
                    state.apply_boop(x, y, dx, dy, placement.piece)
        return state

    def apply_boop(self, x, y, dx, dy, piece):
        nx = x + dx
        ny = y + dy
        if not self.valid_index(nx, ny):
            return
        nloc = self.index_to_loc(nx, ny)
        if self.board[nloc].is_empty():
            return
        if piece is Baip.PieceType.KIT and self.board[nloc].is_cat():
            return
        mx = nx + dx
        my = ny + dy
        if not self.valid_index(mx, my):
            s = self.board[nloc]
            self.board[nloc] = Baip.Square.EMPTY
            player = 0 if s.is_player(0) else 1
            self.pieces[player].Cat += s.is_cat()
            self.pieces[player].Kit += s.is_kit()
        else:
            mloc = self.index_to_loc(mx, my)
            if not self.board[mloc].is_empty():
                return
            self.board[mloc] = self.board[nloc]
            self.board[nloc] = Baip.Square.EMPTY

    def apply_remove(self, x, y):
        loc = self.index_to_loc(x, y)
        state = Baip(self)
        player = self.player
        s = state.board[loc]
        state.pieces[player].Cat += s.is_cat()
        state.pieces[player].Kit += s.is_kit()
        state.board[loc] = Baip.Square.EMPTY
        return state

    def apply_promotion(self, x, y, dx, dy):
        state = Baip(self)
        player = self.player
        for i in range(3):
            s = state.board[self.index_to_loc(x, y)]
            state.pieces[player].TotalCats += s.is_kit()
            state.pieces[player].Cat += 1
            state.board[self.index_to_loc(x, y)] = self.Square.EMPTY
            x += dx
            y += dy
        return state

    def next_turn(self):
        state = Baip(self)
        state.player = 1 if state.player == 0 else 0
        return state

    def is_terminal(self, player=None):
        if player is None:
            player = self.player

        def check(x0, y0, x1, y1, x2, y2):
            a = self.board[self.index_to_loc(x0, y0)]
            b = self.board[self.index_to_loc(x1, y1)]
            c = self.board[self.index_to_loc(x2, y2)]
            return (
                a.is_cat()
                and a.is_player(player)
                and b.is_cat()
                and b.is_player(player)
                and c.is_cat()
                and c.is_player(player)
            )

        def check_vert(x, y):
            return check(x, y - 1, x, y, x, y + 1)

        def check_horz(x, y):
            return check(x - 1, y, x, y, x + 1, y)

        def check_diag(x, y):
            return check(x - 1, y + 1, x, y, x + 1, y - 1) or check(
                x - 1, y - 1, x, y, x + 1, y + 1
            )

        if self.pieces[player].TotalCats == 8 and self.pieces[player].Cat == 0:
            return True
        for y in range(1, self.len_y - 1):
            for x in range(self.len_x):
                if check_vert(x, y):
                    return True
        for y in range(self.len_y):
            for x in range(1, self.len_x - 1):
                if check_horz(x, y):
                    return True
        for y in range(1, self.len_y - 1):
            for x in range(1, self.len_x - 1):
                if check_diag(x, y):
                    return True
        return False

    def print_state(self):
        for y in range(self.len_y):
            for x in range(self.len_x):
                loc = x + y * self.len_x
                print(self.board[loc].to_char(), end="")
            if y == 0:
                print(f"  Player A:{" (current)" if self.player == 0 else ""}")
            if y == 1:
                print(f"    Kittens = {self.pieces[0].Kit}")
            if y == 2:
                print(f"    Cats    = {self.pieces[0].Cat}")
            if y == 3:
                print(f"  Player B:{" (current)" if self.player == 1 else ""}")
            if y == 4:
                print(f"    Kittens = {self.pieces[1].Kit}")
            if y == 5:
                print(f"    Cats    = {self.pieces[1].Cat}")

    len_x: int = 6
    len_y: int = 6
    board: list[Square]
    player: int
    pieces: list[Pieces]
