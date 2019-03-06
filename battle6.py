from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Tuple, Dict

from cachetools import cached

from base_state import BaseStateTurn, Player, BaseMoveTurn, T


@dataclass(frozen=True)
class Card:
    name: str
    can_defend: bool
    can_attack: bool


@dataclass
class Rules:
    cards: List[Card]
    outcomes: Dict[Tuple[Card, Card], Outcome]

    @property
    @cached({})
    def defender(self):
        return tuple(c for c in self.cards if c.can_defend)

    @property
    @cached({})
    def attacker(self):
        return tuple(c for c in self.cards if c.can_attack)

    @classmethod
    def from_data(cls, cards: List[Dict], outcomes: List[Dict[str, str]]):
        cards = {d['name']: Card(**d) for d in cards}
        self = cls(list(cards.values()), {})
        for d in outcomes:
            att_ = cards[d['attack']]
            def_ = cards[d['defend']]
            out_ = {'defend': Outcome.DEF, 'attack': Outcome.ATT, 'tie': Outcome.TIE}[d['outcome']]
            self.outcomes[att_, def_] = out_
        return self

    def __hash__(self):
        return id(self)


class Outcome(Enum):
    ATT = auto()
    DEF = auto()
    TIE = auto()


@dataclass(frozen=True)
class Battle6Move(BaseMoveTurn):
    card: Card


@dataclass(frozen=True)
class Battle6State(BaseStateTurn):
    rules: Rules
    hands: Tuple[Tuple[Card, ...], ...]
    wins: Tuple[int, ...] = (0, 0)
    attack_card: Card = None

    def __post_init__(self):
        assert len(self.players) == 2

    @property
    def is_end(self) -> bool:
        return not bool(self.possible_moves)

    @property
    def winners(self) -> List[Player]:
        assert self.is_end
        if self.wins[0] > self.wins[1]:
            return [self.players[0]]
        elif self.wins[0] < self.wins[1]:
            return [self.players[1]]
        else:
            return []

    @property
    def possible_moves(self) -> List[BaseMoveTurn]:
        if self.attack_card is None:
            return [Battle6Move(self.current_player, c) for c in self.hands[self.current] if c.can_attack]
        else:
            return [Battle6Move(self.current_player, c) for c in self.hands[self.current] if c.can_defend]

    def next_states(self, m: Battle6Move) -> List[Tuple[Battle6State, int]]:
        if self.attack_card is None:
            ahand = tuple(c for c in self.hands[self.current] if c != m.card)
            if self.current == 0:
                hands = (ahand, self.hands[1])
            else:
                hands = (self.hands[0], ahand)
            return [(Battle6State(self.players, (self.current + 1) % 2, self.rules, hands, self.wins, m.card), 1)]
        else:
            dhand = tuple(c for c in self.hands[self.current] if c != m.card)
            if self.current == 0:
                hands = (dhand, self.hands[1])
            else:
                hands = (self.hands[0], dhand)
            r = self.rules.outcomes[(self.attack_card, m.card)]
            aw, ad = self.wins if self.current == 1 else reversed(self.wins)
            if r == Outcome.ATT:
                aw += 1
            elif r == Outcome.DEF:
                ad += 1
            wins = (aw, ad) if self.current == 1 else (ad, aw)
            return [(Battle6State(self.players, (self.current + 1) % 2, self.rules, hands, wins), 1)]

    @classmethod
    def from_rules(cls, rules: Rules, players: Tuple[Player, Player]):
        hands = (tuple(rules.cards), tuple(rules.cards))
        return cls(players, 0, rules, hands)
