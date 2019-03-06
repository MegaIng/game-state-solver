from dataclasses import dataclass
from typing import List, Tuple

from base_state import BaseState, BaseMove, T, Player, BaseStateTurn, BaseMoveTurn


@dataclass(frozen=True)
class StickMove(BaseMoveTurn):
    n: int


@dataclass(frozen=True)
class StickState(BaseStateTurn):
    players: Tuple[Player, ...]
    current: int
    sticks: int
    __slots__ = ('players', 'current', 'sticks', '_moves')

    def __post_init__(self):
        super().__setattr__('_moves', [StickMove(p, n) for n in range(1, 5) for p in self.players])

    @property
    def is_end(self) -> bool:
        return self.sticks <= 0

    @property
    def winners(self) -> List[Player]:
        assert self.is_end
        return [self.players[(self.current - 1) % len(self.players)]]

    @property
    def possible_moves(self) -> List[StickMove]:
        return self._moves[self.current:self.sticks * len(self.players):len(self.players)]

    def next_states(self: T, m: StickMove) -> List[Tuple[T, float]]:
        return [(StickState(self.players, (self.current - 1) % len(self.players), self.sticks - m.n), 1)]
