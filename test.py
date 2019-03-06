import json
from pprint import pprint

from base_state import Player
from best_moves import best_moves_turn, Assumptions, Behaviour
from battle6 import Battle6State, Rules

rules = Rules.from_data(**json.load(open('battle6.json')))
# print(rules)
ss = Battle6State.from_rules(rules, (Player('A'), Player('B')))

# pprint(ss.possible_moves)
pprint(best_moves_turn(ss, Player('A'), Assumptions(Behaviour.OPTIMAL, Behaviour.RANDOM)))
pprint(best_moves_turn(ss, Player('B'), Assumptions(Behaviour.OPTIMAL, Behaviour.RANDOM)))
