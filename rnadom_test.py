import copy
import time
import random

import statistics

import matplotlib.pyplot as plt

import sys
# sys.path.append("D:/Project/multi-quoridor-alphazero")
sys.path.append("../")

from game import State
import huristic_evaluation as huristic_evaluation


class MyState(State):
    def __init__(self, state=None):
        if state == None:
            super().__init__()
        else:
            super().__init__(state.player, state.turn)

    def is_end(self):
        return self.is_done()
    
    def generate_states(self):
        actions = self.legal_actions()
        return [MyState(copy.deepcopy(self).next(action)) for action in actions]

    def evaluate(self):
        return huristic_evaluation.huristic_5(self)
    
    def get_left_wall(self, turn):
        count = len(self.player[turn][2]) + \
            len(self.player[turn][3])
        return 5 - count
    
    def is_draw(self):
        return self.turn > 1000

    

def random_play(state: MyState, p=True):
    if p:
        print("random play")

    next_states = state.generate_states()

    if len(next_states) == 0:
        return state
    else:
        return random.choice(state.generate_states())

def play(state: MyState, player, time_list=None, p=True):
    state = copy.deepcopy(state)

    if p:
        print(f"turn: {state.turn}", flush=True)

    start = time.time()
    next_state = player(state, p)
    end = time.time()

    run_time = end - start
    if time_list is not None:
        time_list.append(run_time)
    
    if p:
        print(f"{run_time:.5f} sec", flush=True)
        print(str(next_state), end='', flush=True)
        print("------------------------------------", flush=True)
    
    return next_state

if __name__ == "__main__":
    # now_state= MyState()

    # print(str(now_state), end='')
    # print("------------------------------------")
    time_list = []
    turn_list = []
    r = 10000
    wc = [0, 0, 0, 0, 0]
    for i in range(r):
        now_state= MyState()
        
        while(not now_state.is_end()):
            now_state = play(now_state, random_play, p=False)
            if now_state.is_end():
                break

            now_state = play(now_state, random_play, p=False)
            if now_state.is_end():
                break

            now_state = play(now_state, random_play, p=False)
            if now_state.is_end():
                break

            now_state = play(now_state, random_play, p=False)
            
        # print(f"\n{now_state.winner()} win!\n")
        
        # sum = 0
        # count = 0
        # for t in time_list:
        #     print(f"{t:.5f}", end=' ')
        #     sum += t
        #     count += 1
        # print(f"\nsum: {sum:.5f}, count: {count}")
        # print(f"avg: {sum/count:.5f}")

        if now_state.winner() != -1:
            wc[now_state.winner()] += 1
        else:
            wc[4] += 1

        turn_list.append(now_state.turn)

        if len(turn_list) >= 2:
            print(f"\r{turn_list[-1]}, {statistics.mean(turn_list):.5f}, {statistics.stdev(turn_list):.5f}")
        
    print(f"{statistics.mean(turn_list):.5f}, {statistics.stdev(turn_list):.5f}")

    plt.hist(turn_list)