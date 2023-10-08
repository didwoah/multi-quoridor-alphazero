from game import State
import random as rd
from tqdm import tqdm

def random_action(state):
    legal_actions = state.legal_actions()
    if len(legal_actions) == 0:
        return None
    return legal_actions[rd.randint(0, len(legal_actions) - 1)]

def playout(state):

    if state.is_done():

        if state.is_draw():
            return [0.25 for _ in range(4)]
        
        rlst = [0] * 4
        rlst[state.winner()] += 1
        return rlst
    
    return playout(state.next(random_action(state)))

def argmax(collection, key=None):
    return collection.index(max(collection))

def mcs_action(state):

    p = state.get_player()
    legal_actions = state.legal_actions()
    values = [0] * len(legal_actions)
    for i, action in enumerate(legal_actions):
        for _ in range(1):
            res = playout(state.next(action))
            values[i] += res[p]

    # print(values)
    return legal_actions[argmax(values)]