from game import State
from pv_mcts import pv_mtcs_scores
from model import DN_OUTPUT_SIZE, resnet
from datetime import datetime
import numpy as np
import pickle
import os
import torch
from tqdm import tqdm

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
        for action, policy in zip(state.legal_actions(True), scores):
            polices[action] = policy
        history.append([state.get_input_state(), polices, None])

        action = np.random.choice(state.legal_actions(True), p=scores)

        state = state.next(action, True)

    values = get_values(state)
    for i in range(len(history)):
        history[i][2] = values
        tmp = []
        tmp.extend(values[1:])
        tmp.append(values[0])
        values = tmp
    return history

def self_play(model):
    history = []

    for _ in tqdm(range(SP_GAME_COUNT)):
        h = play(model)
        history.extend(h)

    write_data(history)

if __name__ == '__main__':
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)
    model = resnet()
    model.load_state_dict(torch.load('./model/chekpoint1.pth'))
    model = model.to(device)
    model.eval()
    self_play(model)