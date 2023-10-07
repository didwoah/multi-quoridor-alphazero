from QuoridorAPI import State
import torch
from model import resnet
from pv_mcts import pv_mcts_action
from max_n import max_n_action
from mcts import random_action, mcts_action

EP_GAME_COUNT = 10

def get_values(state):
    if state.is_draw():
            return [0.25 for _ in range(4)]
        
    rlst = [0] * 4
    rlst[state.winner()] += 1
    return rlst

def play(next_actions):
    state = State()

    while True:
        if state.is_done():
            break

        next_action = next_actions[0] if state.is_first_player() else next_actions[1]
        action = next_action(state)

        state = state.next(action)

    return get_values(state)

def change_turn(collection):
    return collection[1:] , collection[0]

def evaluate_algorithm_of(label, next_actions):

    total_point = 0

    for i in range(EP_GAME_COUNT):
        total_point += play(next_actions)[i % 4]
        change_turn(next_actions)

        print('\rEvaluate {}/{}'.format(i+1, EP_GAME_COUNT), end='')
    print('')

    average_point = total_point / EP_GAME_COUNT
    print(label.format(average_point))

def evaluate_best_player():
    model = resnet()
    model.load_state_dict(torch.load('your_model_checkpoint.pth'))
    model.eval() 

    next_pv_mcts_action = pv_mcts_action(model, 0.0)

    next_actions = (next_pv_mcts_action, random_action, random_action, random_action)
    evaluate_algorithm_of('VS_RANDOM', next_actions)

    next_actions = (next_pv_mcts_action, max_n_action, max_n_action, max_n_action)
    evaluate_algorithm_of('VS_MAX_N', next_actions)

    next_actions = (next_pv_mcts_action, mcts_action, mcts_action, mcts_action)
    evaluate_algorithm_of('VS_MCTS', next_actions)


if __name__ == '__main__':
    evaluate_best_player()