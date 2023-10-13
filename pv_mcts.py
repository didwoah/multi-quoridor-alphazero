import math
from game import State
import numpy as np
import copy
from model import resnet, DN_INPUT_SHAPE
import torch
from tqdm import tqdm

PARENT_NODE_COUNT = 1
PV_EVALUATE_COUNT = 1600



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
    values = y[0][0] # 2 3 4 1

    player = state.get_player()
    values = torch.concat((values[4-player:], values[:4-player]), dim=0) # 0 1 2 3
    
    return polices, values

def nodes_to_scores(nodes):
    scores = []
    for c in nodes:
        scores.append(c.n)
    return scores

def argmax(collection):
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
                self.child_nodes = [ Node(self.state.next(action, True)) for action in self.state.legal_actions(True) ]
            else:
                self.child_nodes = [ Node(self.state.next(action, True)) for action in legal_actions ]
        
        def eval(self):
            if self.state.is_done():

                scores = [0.25 for _ in range(4)]
                if not self.state.is_draw():
                    winner = self.state.winner()
                    scores = [0 for _ in range(4)]
                    scores[winner] = 1

                self.scores = [self.scores[i] + scores[i] for i in range(4)]
                self.n += 1

                return self.scores
            if not self.child_nodes:

                _, values = predict(model, self.state)
                self.scores = [self.scores[i] + values[i] for i in range(4)]
                self.n += 1

                if self.n == PARENT_NODE_COUNT:
                    self.expand()

                return values
            else:
                child_scores = self.next_child_node().eval()

                self.scores = [self.scores[i] + child_scores[i] for i in range(4)]
                self.n += 1
                return child_scores

    legal_actions = state.legal_actions(True)
    if len(legal_actions) == 0:
        return None
    
    root_node = Node(state)
    root_node.expand(legal_actions)

    for _ in range(PV_EVALUATE_COUNT):
        root_node.eval()

    scores = nodes_to_scores(root_node.child_nodes)
    if temperature < 0.001:
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
    sum_xs = sum(xs)
    if sum_xs == 0:
        return [1 / len(xs) for _ in xs]
    return [x / sum_xs for x in xs]

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