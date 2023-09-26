from game import State
from pv_mtcs import pv_mtcs_scores
from dual_network import DN_OUTPUT_SIZE
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from pathlib import Path
import numpy as np
import pickle
import os

SP_GAME_COUNT = 10
SP_TEMPERATURE = 1.0

def first_player_value(ended_state):
    if ended_state.is_lose():
        return -1 if ended_state.is_first_player() else 1
    return 0

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
        history.append([[state.pieces, state.enemy_pieces,], polices, None])

        action = np.random.choice(state.legal_actions(), p=scores)

        state = state.next(action)

    value = first_player_value(state)
    for i in range(len(history)):
        history[i][2] = value
        value = -value
    return history

def self_play():
    history = []

    model = load_model('./model/best.h5')

    for i in range(SP_GAME_COUNT):
        h = play(model)
        history.extend(h)

        print('\rSelfPlay {}/{}'.format(i+1, SP_GAME_COUNT), end='')
    print('')

    write_data(history)
    K.clear_session()
    del model

if __name__ == '__main__':
    self_play()
