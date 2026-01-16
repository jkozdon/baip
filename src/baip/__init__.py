# TODO: Promotions
#       - three cats / kittens in a row
#       - Possible choice for resolution
# TODO: [optional] Add ability to check if move is valid

from dataclasses import dataclass
from enum import Enum, auto
import random


LEN_X = 8
LEN_Y = 8


def valid_coord(x: int, y: int) -> bool:
    return x >= 0 and x < LEN_X and y >= 0 and y < LEN_Y


def coord_to_index(x: int, y: int) -> int:
    return x + y * LEN_X


def index_to_coord(index: int) -> tuple[int, int]:
    x = index % LEN_X
    y = index // LEN_X
    return (x, y)


class Phase(Enum):
    TERMINAL = auto()
    SPECIAL = auto()
    PLACEMENT = auto()


@dataclass(frozen=True)
class Action:
    """Base class for all action types."""

    pass


class PieceType(Enum):
    KIT = auto()
    CAT = auto()


@dataclass(frozen=True)
class Placement(Action):
    x: int
    y: int
    piece: PieceType


@dataclass(frozen=True)
class Removal(Action):
    x: int
    y: int


@dataclass(frozen=True)
class Promotion(Action):
    squares: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]


class Square(Enum):
    EMPTY = auto()
    KIT_A = auto()
    CAT_A = auto()
    KIT_B = auto()
    CAT_B = auto()

    def to_char(self):
        if self is Square.EMPTY:
            return "."
        if self is Square.KIT_A:
            return "a"
        if self is Square.CAT_A:
            return "A"
        if self is Square.KIT_B:
            return "b"
        if self is Square.CAT_B:
            return "B"


@dataclass(frozen=True)
class Pieces:
    kittens_remaining: int
    cats_remaining: int
    total_cats: int


@dataclass(frozen=True)
class State:
    active_player: int
    board: tuple[Square, ...]
    pieces: tuple[Pieces, Pieces]
    phase: Phase
    turn_counter: int


def initial_state() -> State:
    board = tuple(Square.EMPTY for _ in range(LEN_X * LEN_Y))
    init_piece = Pieces(kittens_remaining=8, cats_remaining=0, total_cats=0)
    pieces = (init_piece, init_piece)
    return State(
        active_player=0,
        board=board,
        pieces=pieces,
        turn_counter=0,
        phase=Phase.PLACEMENT,
    )


def print_state(state) -> None:
    print(f"Active player: {state.active_player}")
    print(f"turn counters: {state.turn_counter}")
    for player in range(2):
        print()
        print(f"Player {player} pieces:")
        print(f"  kittens:     {state.pieces[player].kittens_remaining}")
        print(f"  cat:         {state.pieces[player].cats_remaining}")
        print(f"  total cats:  {state.pieces[player].total_cats}")

    print()
    print("  ", end="")
    for x in range(LEN_X):
        print(x, end="")
    print()
    print(" +--------")
    for y in range(LEN_Y):
        print(f"{y}|", end="")
        for x in range(LEN_X):
            index = coord_to_index(x, y)
            print(state.board[index].to_char(), end="")
        print()


def is_terminal(state: State) -> bool:
    player = state.active_player
    if (
        state.pieces[player].total_cats == 8
        and state.pieces[player].cats_remaining == 0
    ):
        print(f"Player {"a" if player == 0 else "b"} placed all cats")
        return True

    board = state.board
    cat = Square.CAT_A if player == 0 else Square.CAT_B

    def check(squares):
        for x, y in squares:
            if not valid_coord(x, y):
                return False
            loc = coord_to_index(x, y)
            if board[loc] != cat:
                return False
        return True

    dirs = [(0, 1), (1, 1), (1, 0), (-1, 1)]
    for y in range(LEN_Y):
        for x in range(LEN_X):
            for dir in dirs:
                dx = dir[0]
                dy = dir[1]
                squares = (
                    (x, y),
                    (x + dx, y + dy),
                    (x + 2 * dx, y + 2 * dy),
                )
                if check(squares):
                    ps = "a" if player == 0 else "b"
                    print(f"Player {ps} has cats {squares}")
                    return True
    return False


def get_legal_placements(state: State) -> list[Placement]:
    actions = []
    has_kittens = state.pieces[state.active_player].kittens_remaining > 0
    has_cats = state.pieces[state.active_player].cats_remaining > 0
    for y in range(LEN_Y):
        for x in range(LEN_Y):
            index = coord_to_index(x, y)
            if state.board[index] is Square.EMPTY:
                if has_kittens:
                    p = Placement(x=x, y=y, piece=PieceType.KIT)
                    actions.append(p)
                if has_cats:
                    p = Placement(x=x, y=y, piece=PieceType.CAT)
                    actions.append(p)
    return actions


def get_legal_promotions(state) -> list[Promotion]:
    player = state.active_player
    board = state.board
    kitcats = (
        (Square.KIT_A, Square.CAT_A)
        if player == 0
        else (Square.KIT_B, Square.CAT_B)
    )

    def check(prom):
        for x, y in prom.squares:
            if not valid_coord(x, y):
                return False
            loc = coord_to_index(x, y)
            if board[loc] not in kitcats:
                return False
        return True

    dirs = [(0, 1), (1, 1), (1, 0), (-1, 1)]
    promotions = []
    for y in range(LEN_Y):
        for x in range(LEN_X):
            for dir in dirs:
                dx = dir[0]
                dy = dir[1]
                prom = Promotion(
                    (
                        (x, y),
                        (x + dx, y + dy),
                        (x + 2 * dx, y + 2 * dy),
                    )
                )
                if check(prom):
                    promotions.append(prom)
    return promotions


def get_legal_removes(state) -> list[Removal]:
    player = state.active_player
    if (
        state.pieces[player].cats_remaining > 0
        or state.pieces[player].kittens_remaining > 0
    ):
        return []
    removal = []
    board = state.board
    kitcats = (
        (Square.KIT_A, Square.CAT_A)
        if player == 0
        else (Square.KIT_B, Square.CAT_B)
    )
    for y in range(LEN_Y):
        for x in range(LEN_X):
            index = coord_to_index(x, y)
            if board[index] in kitcats:
                removal.append(Removal(x, y))
    return removal


def get_legal_actions(state: State) -> list[Action]:
    if state.phase is Phase.PLACEMENT:
        return get_legal_placements(state)
    else:
        promotions = get_legal_promotions(state)
        removes = get_legal_removes(state)
        return promotions + removes


def apply_promotion(state: State, promotion: Promotion) -> State:
    player = state.active_player
    p = state.pieces[player]
    kittens_remaining = p.kittens_remaining
    cats_remaining = p.cats_remaining
    total_cats = p.total_cats
    board = list(state.board)
    for x, y in promotion.squares:
        index = coord_to_index(x, y)
        if board[index] == Square.KIT_A or board[index] == Square.KIT_B:
            total_cats += 1
        cats_remaining += 1
        board[index] = Square.EMPTY

    next_player = 1 if player == 0 else 0
    next_turn_count = state.turn_counter + player
    pieces = list(state.pieces)
    pieces[player] = Pieces(
        kittens_remaining=kittens_remaining,
        cats_remaining=cats_remaining,
        total_cats=total_cats,
    )
    return State(
        active_player=next_player,
        board=tuple(board),
        pieces=tuple(pieces),
        phase=Phase.PLACEMENT,
        turn_counter=next_turn_count,
    )


def apply_removal(state: State, removal: Removal) -> State:
    player = state.active_player
    board = list(state.board)
    index = coord_to_index(removal.x, removal.y)
    square = board[index]
    board[index] = Square.EMPTY
    pieces = list(state.pieces)
    total_cats = pieces[player].total_cats
    if square in (Square.KIT_A, square.KIT_B):
        total_cats += 1
    pieces[player] = Pieces(
        kittens_remaining=0, cats_remaining=1, total_cats=total_cats
    )

    next_player = 1 if player == 0 else 0
    next_turn_count = state.turn_counter + player
    return State(
        active_player=next_player,
        board=tuple(board),
        pieces=tuple(pieces),
        phase=Phase.PLACEMENT,
        turn_counter=next_turn_count,
    )


def apply_boop(board, pieces, x, y, dx, dy, is_cat) -> None:
    nx = x + dx
    ny = y + dy
    if not valid_coord(nx, ny):
        return
    nindex = coord_to_index(nx, ny)

    square = board[nindex]
    if square == Square.EMPTY or (
        not is_cat and (square == Square.CAT_A or square == Square.CAT_B)
    ):
        return

    nnx = nx + dx
    nny = ny + dy
    if not valid_coord(nnx, nny):
        board[nindex] = Square.EMPTY
        if square == Square.KIT_A:
            p = pieces[0]
            pieces[0] = Pieces(
                kittens_remaining=p.kittens_remaining + 1,
                cats_remaining=p.cats_remaining,
                total_cats=p.total_cats,
            )
        elif square == Square.CAT_A:
            p = pieces[0]
            pieces[0] = Pieces(
                kittens_remaining=p.kittens_remaining,
                cats_remaining=p.cats_remaining + 1,
                total_cats=p.total_cats,
            )
        elif square == Square.KIT_B:
            p = pieces[1]
            pieces[1] = Pieces(
                kittens_remaining=p.kittens_remaining + 1,
                cats_remaining=p.cats_remaining,
                total_cats=p.total_cats,
            )
        elif square == Square.CAT_B:
            p = pieces[1]
            pieces[1] = Pieces(
                kittens_remaining=p.kittens_remaining,
                cats_remaining=p.cats_remaining + 1,
                total_cats=p.total_cats,
            )
        return

    nnindex = coord_to_index(nnx, nny)
    if board[nnindex] == Square.EMPTY:
        board[nnindex] = square
        board[nindex] = Square.EMPTY


def apply_placement(state: State, placement: Placement) -> State:
    place_cat = placement.piece == PieceType.CAT
    player = state.active_player
    board = list(state.board)
    index = coord_to_index(placement.x, placement.y)
    if player == 0:
        board[index] = Square.CAT_A if place_cat else Square.KIT_A
    else:
        board[index] = Square.CAT_B if place_cat else Square.KIT_B
    pieces = list(state.pieces)
    pieces[player] = Pieces(
        kittens_remaining=pieces[player].kittens_remaining - (not place_cat),
        cats_remaining=pieces[player].cats_remaining - place_cat,
        total_cats=pieces[player].total_cats,
    )
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            apply_boop(
                board, pieces, placement.x, placement.y, dx, dy, place_cat
            )

    state = State(
        active_player=player,
        board=tuple(board),
        pieces=tuple(pieces),
        phase=Phase.SPECIAL,
        turn_counter=state.turn_counter,
    )

    if is_terminal(state):
        return State(
            active_player=player,
            board=tuple(board),
            pieces=tuple(pieces),
            phase=Phase.TERMINAL,
            turn_counter=state.turn_counter,
        )

    actions = get_legal_actions(state)

    if len(actions) == 0:
        state = State(
            active_player=1 if state.active_player == 0 else 1,
            board=state.board,
            pieces=state.pieces,
            phase=Phase.PLACEMENT,
            turn_counter=state.turn_counter + state.active_player,
        )
    elif len(actions) == 1:
        state = apply_action(state, actions[0])

    return state


# TODO: implement for real!
def apply_action(state: State, action: Action) -> State:
    if type(action) is Placement:
        return apply_placement(state, action)
    elif type(action) is Promotion:
        return apply_promotion(state, action)
    elif type(action) is Removal:
        return apply_removal(state, action)
    else:
        raise ValueError("invalid action")


# TODO: implement for real!
def get_result(state: State) -> float:
    pass
