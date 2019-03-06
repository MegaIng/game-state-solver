from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, TypeVar


@dataclass(frozen=True)
class Player:
    name: str
    __slots__ = ('name',)


@dataclass(frozen=True)
class BaseMove(ABC):
    __slots__ = ()


T = TypeVar('T')


@dataclass(frozen=True)
class BaseState(ABC):
    players: Tuple[Player, ...]
    __slots__ = ('players',)

    @property
    @abstractmethod
    def is_end(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def winners(self) -> List[Player]:
        raise NotImplementedError

    @property
    @abstractmethod
    def possible_moves(self) -> List[BaseMove]:
        raise NotImplementedError

    @abstractmethod
    def next_states(self: T, m: BaseMove) -> List[Tuple[T, int]]:
        raise NotImplementedError


@dataclass(frozen=True)
class BaseMoveTurn(BaseMove):
    player: Player
    __slots__ = ('player',)


@dataclass(frozen=True)
class BaseStateTurn(BaseState, ABC):
    current: int

    @property
    def current_player(self):
        return self.players[self.current]

    @property
    @abstractmethod
    def possible_moves(self) -> List[BaseMoveTurn]:
        raise NotImplementedError

    @abstractmethod
    def next_states(self: T, m: BaseMoveTurn) -> List[Tuple[T, int]]:
        raise NotImplementedError
