from QuoridorAPI import State
from pv_mcts import pv_mtcs_scores
from model import DN_OUTPUT_SIZE
from datetime import datetime
import numpy as np
import pickle
import os

SP_GAME_COUNT = 10
SP_TEMPERATURE = 1.0

def get_values(state):
    if state.is_draw():
            return [0.25 for _ in range(4)]
        
    rlst = [0] * 4
    rlst[state.winner()] += 1
    return rlst

def write_data(history):
    now = datetime.now()
    os.makedirs('./data/', exist_ok=True)
    path = './data/{:04}{:02}{:02}{:02}{:02}{:02}.history'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    with open(path, mode='wb') as f:
        pickle.dump(history, f)

def play(model):
    history = []
    state = State()
    while True:
        if state.is_done():
            break
        
        scores = pv_mtcs_scores(model, state, SP_TEMPERATURE)

        polices = [0] * DN_OUTPUT_SIZE
        for action, policy in zip(state.legal_actions(), scores):
            polices[action] = policy
        history.append([state.get_input_state(), polices, None])

        action = np.random.choice(state.legal_actions(), p=scores)

        state = state.next(action)

    values = get_values(state)
    for i in range(len(history)):
        history[i][2] = values
    return history

def self_play():
    history = []

    for i in range(SP_GAME_COUNT):
        h = play(model)
        history.extend(h)

        print('\rSelfPlay {}/{}'.format(i+1, SP_GAME_COUNT), end='')
    print('')

    write_data(history)
    del model

if __name__ == '__main__':
    self_play()
