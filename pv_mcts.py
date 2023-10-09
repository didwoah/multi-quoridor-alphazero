import math
from game import State
import numpy as np
import copy
from model import resnet, DN_INPUT_SHAPE
import torch
from tqdm import tqdm

PARENT_NODE_COUNT = 3
PV_EVALUATE_COUNT = 1000

def predict(model, state: State):

    a, b, c = DN_INPUT_SHAPE

    x = state.get_input_state() # 회전한 input을 받는다
    x =  torch.tensor(x, dtype=torch.float32)
    x = x.reshape(1, a, b, c)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    x = x.to(device)
    y = model(x) 

    polices = y[1][0][list(state.legal_actions(is_alpha_zero=True))] # 상대적 움직임에 대한 정책
    polices /= sum(polices) if sum(polices) else 1
    values = y[0][0]
    
    return polices, values

def nodes_to_scores(nodes):
    scores = []
    for c in nodes:
        scores.append(c.n)
    return scores

def argmax(collection, key=None):
    return collection.index(max(collection))

def pv_mtcs_scores(model, state, temperature):
    class Node:
        def __init__(self, state):
            self.state = copy.deepcopy(state)
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
                self.child_nodes = [ Node(copy.deepcopy(self.state).next(action, True)) for action in self.state.legal_actions(True) ]
            else:
                self.child_nodes = [ Node(copy.deepcopy(self.state).next(action, True)) for action in legal_actions ]
        
        def eval(self):
            if self.state.is_done():
                if self.state.is_draw():
                    self.scores = [0.25 for _ in range(4)]
                else:
                    winner = self.state.winner()
                    self.scores = [0 for _ in range(4)]
                    self.scores[winner] += 1
                return self.scores

            if not self.child_nodes:

                _, values = predict(model, self.state)
                self.scores = [self.scores[i] + values[i] for i in range(4)]
                self.n += 1

                if self.n == PARENT_NODE_COUNT:
                    self.expand()
                return self.scores
            else:
                ncn = self.next_child_node()
                # print("c",ncn.state.player)
                child_scores = ncn.eval()

                player = self.state.get_player()

                if self.scores[player] < child_scores[player]:
                    self.scores = child_scores
                self.n += 1

                return child_scores

    root_node = Node(state)

    for _ in tqdm(range(PV_EVALUATE_COUNT)):
        # print(root_node.state.player)
        root_node.eval()

    scores = nodes_to_scores(root_node.child_nodes)
    if temperature == 0:
        action = np.argmax(scores)
        scores = np.zeros(len(scores))
        scores[action] = 1
    else:
        scores = boltzman(scores, temperature)
    return scores

def pv_mcts_action(model, temperature = 0):
    def pv_mcts_action(state):
        scores = pv_mtcs_scores(model, state, temperature)
        return np.random.choice(state.legal_actions(True), p=scores)
    
    return pv_mcts_action

def boltzman(xs, temperature):
    xs = [x ** (1/temperature) for x in xs]
    return [x / sum(xs) for x in xs]

if __name__ == '__main__':

    model  = resnet()
    model.eval()

    state = State()

    next_action = pv_mcts_action(model, 1.0)

    while True:

        if state.is_done():
            break

        action = next_action(state) # 최적 상대적 움직임

        state = state.next(action, is_alpha_zero=True) # 상대적 움직임에 대한 다음 상태

        print(state)