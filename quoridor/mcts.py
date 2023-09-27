import numpy as np
import random as rd
import math
import copy
from QuoridorAPI import State

PLAYOUT_LIMIT = 10
MCTS_CNT = 5000
PLAYOUT_CNT = 50


class Node:
    def __init__(self, state, action=None):
        self.state = copy.deepcopy(state)
        self.action = copy.deepcopy(action)
        self.n = 0
        self.w = 0
        self.scores = [0, 0, 0, 0]
        self.children = []  # list of Node

    def expand(self):
        self.children = [Node(self.state.next(action), action)
                         for action in self.state.legal_actions()]

    def findFinalMove(self):
        bestNext = None
        bestN = 0
        for child in self.children:
            if bestN < child.n:
                bestN = child.n
                bestNext = child
        return bestNext


def UCT(node, n_parent):
    w, n = node.w, node.n
    c = 0.2
    if n == 0:
        return math.inf
    return w/n + c * ((math.log(n_parent) / n)**0.5)


def playout(node):
    win_list = np.array([0, 0, 0, 0])
    for _ in range(PLAYOUT_CNT):
        currentState = copy.deepcopy(node.state)
        while True:
            actions = currentState.legal_actions()
            # print(actions)
            random_action = rd.choice(actions)
            currentState = currentState.next(random_action)
            if currentState.is_done():
                if currentState.is_draw:
                    break
                winner = currentState.winner()
                win_list[winner] += 1
                break
    win_list = win_list / PLAYOUT_CNT
    return win_list


def MCTS(node, currentPlayer):
    if len(node.children) == 0 and node.n == PLAYOUT_LIMIT:
        node.expand()

    if len(node.children) == 0:
        # terminal node - playout
        result = playout(node)  # tuple (s1,s2,s3,s4)
        node.scores = result
        node.w = result[currentPlayer]
        node.n += 1
        return result

    else:
        bestChild = None
        bestChildUCT = 0
        for idx, child in enumerate(node.children):
            uct = UCT(child, node.n)
            if uct > bestChildUCT:
                bestChildUCT = uct
                bestChild = child

        result = MCTS(bestChild, (currentPlayer + 1) % 4)

        if result[currentPlayer] > node.scores[currentPlayer]:
            node.scores = result
            node.w = result[currentPlayer]
        node.n += 1

        return node.scores


if __name__ == '__main__':
    root = Node(State())
    root.expand()
    rootPlayer = 0
    for i in range(MCTS_CNT):
        print('\r{}/{}'.format(i, MCTS_CNT))
        result = MCTS(root, rootPlayer)

    print(root.findFinalMove().action)
