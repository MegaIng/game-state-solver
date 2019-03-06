from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict

from cachetools import cached

from base_state import Player, BaseStateTurn, BaseMoveTurn


class Behaviour(Enum):
    OPTIMAL = auto()
    ANTI_OPTIMAL = auto()
    RANDOM = auto()


@dataclass(frozen=True)
class Assumptions:
    player_behaviour: Behaviour
    opponents_behaviour: Behaviour


# @cached({})
def best_moves_turn(s: BaseStateTurn, player: Player, ass: Assumptions) -> Dict[BaseMoveTurn, float]:
    result = {}
    for m in s.possible_moves:
        data = []
        for n, w in s.next_states(m):
            if n.is_end:
                if player in n.winners:
                    data.append((1, w))
                else:
                    data.append((0, w))
            else:
                bm = best_moves_turn(n, player, ass)
                if not bm:
                    print(n)
                if n.current_player == player:
                    assert all(cm.player == player for cm in bm)
                    if ass.player_behaviour == Behaviour.OPTIMAL:
                        data.append((max(bm.values()), w))
                    elif ass.player_behaviour == Behaviour.ANTI_OPTIMAL:
                        data.append((min(bm.values()), w))
                    else:
                        data.append((sum(bm.values()) / len(bm), w))
                else:
                    assert all(cm.player != player for cm in bm)
                    if ass.opponents_behaviour == Behaviour.OPTIMAL:
                        data.append((min(bm.values()), w))
                    elif ass.opponents_behaviour == Behaviour.ANTI_OPTIMAL:
                        data.append((max(bm.values()), w))
                    else:
                        data.append((sum(bm.values()) / len(bm), w))
        result[m] = sum(v * w for v, w in data) / sum(w for _, w in data)
    # print(s, result)
    return result
