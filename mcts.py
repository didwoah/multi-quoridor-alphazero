import numpy as np
import random as rd
import math
import copy
from game import State
import time
# from tqdm import tqdm


PARENT_NODE_COUNT = 3
PV_EVALUATE_COUNT = 1000


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
        rlst[state.winner()] = 1
        return rlst
    
    return playout(state.next(random_action(state)))

def argmax(collection):
    return collection.index(max(collection))

def mcts_action(state):
    class Node:
        def __init__(self, state):
            self.state = state
            self.n = 0
            self.scores = [0,0,0,0]
            self.child_nodes = None

        def get_parent_score(self):
            parent_turn = (self.state.get_player() + 3) % 4
            return self.scores[parent_turn]

        def next_child_node(self):
            for child_node in self.child_nodes:
                if child_node.n == 0:
                    return child_node

            t = 0
            for c in self.child_nodes:
                t += c.n
            ucb1_values = []
            for child_node in self.child_nodes:
                ucb1_values.append(child_node.get_parent_score() / child_node.n + (2 * math.log(t) / child_node.n) ** 0.5)

            return self.child_nodes[argmax(ucb1_values)]

        def expand(self, legal_actions = None):
            if not legal_actions:
                self.child_nodes = [ Node(self.state.next(action)) for action in self.state.legal_actions() ]
            else:
                self.child_nodes = [ Node(self.state.next(action)) for action in legal_actions ]
        
        def eval(self):
            if self.state.is_done():

                scores = [0.25] * 4

                if not self.state.is_draw():
                    winner = self.state.winner()
                    scores = [0] * 4
                    scores[winner] = 1

                self.scores = [self.scores[i] + scores[i] for i in range(4)]
                self.n += 1

                return scores
            if not self.child_nodes:

                scores = playout(self.state)
                self.scores = [self.scores[i] + scores[i] for i in range(4)]
                self.n += 1

                if self.n == PARENT_NODE_COUNT:
                    self.expand()

                # note
                # return self.scores
                return scores
            else:
                child_scores = self.next_child_node().eval()

                # note
                # self.scores가 조금 더 잘 바뀌려면 졌을 때 -1을 해줘야할 수도 있음 실험 예정
                # player = self.state.get_player()
                # if self.scores[player] < child_scores[player]:
                #     self.scores = child_scores

                self.scores = [self.scores[i] + child_scores[i] for i in range(4)]
                self.n += 1
                return child_scores

    legal_actions = state.legal_actions()
    if len(legal_actions) == 0:
        return None
            
    root_node = Node(state)
    root_node.expand(legal_actions)

    for _ in range(PV_EVALUATE_COUNT):
        root_node.eval()

    n_list = []
    for c in root_node.child_nodes:
        n_list.append(c.n)
    return legal_actions[argmax(n_list)]


EP_GANE_COUNT = 10

def play(next_actions):
    state = State()

    while True:

        if state.is_done():
            break

        next_action = next_actions[state.get_player()]
        action = next_action(state)
        state = state.next(action)

    if state.is_draw():
        return [0.25 for _ in range(4)]
    
    rlst = [0] * 4
    rlst[state.winner()] += 1
    return rlst

def change_turn(collection):
    rlst = []
    rlst.extend(collection[1:])
    rlst.extend([collection[0]])
    return rlst

def evaluate_algorithm_of(label, next_actions):

    total_point = 0

    for i in range(EP_GANE_COUNT):
        total_point += play(next_actions)[i % 4]
        next_actions = change_turn(next_actions)

    average_point = total_point / EP_GANE_COUNT
    print('')
    print(label.format(average_point))

if __name__ == '__main__':
    next_actions = [mcts_action, random_action, random_action, random_action]
    evaluate_algorithm_of('VS_RANDOM {:3f}', next_actions)