# TODO: Promotions
#       - three cats / kittens in a row
#       - Possible choice for resolution
# TODO: [optional] Add ability to check if move is valid

from dataclasses import dataclass
from enum import Enum, auto
import random


LEN_X = 8
LEN_Y = 8


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


@dataclass(frozen=True)
class Pieces:
    kittens_remaining: int
    cats_remaining: int
    cats_on_board: int


@dataclass(frozen=True)
class State:
    active_player: int
    board: tuple[Square, ...]
    pieces: tuple[Pieces, Pieces]
    turn_counter: int


def initial_state() -> State:
    board = tuple(Square.EMPTY for _ in range(LEN_X * LEN_Y))
    init_piece = Pieces(kittens_remaining=8, cats_remaining=0, cats_on_board=0)
    pieces = (init_piece, init_piece)
    return State(active_player=0, board=board, pieces=pieces, turn_counter=0)


# TODO: implement for real!
def is_terminal(state: State) -> bool:
    return random.choice((True, False))


# TODO: implement for real!
def get_legal_actions(state: State) -> list[Action]:
    return (None)


# TODO: implement for real!
def apply_action(state: State, action: Action) -> State:
    pass


# TODO: implement for real!
def get_result(state: State) -> float:
    pass
