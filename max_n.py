import copy
import time
import random

import sys
# sys.path.append("D:/Project/multi-quoridor-alphazero")
sys.path.append("../")

from game import State
from huristic_evaluation import huristic_5 as huristic

def max_n(now_state: State, depth):
    now_state = copy.deepcopy(now_state)

    if depth == 0 or now_state.is_done():
        return huristic(now_state), now_state
    
    best_val = -float('inf')
    best_state = None
    best_vals = None

    next_states = [now_state.next(action) for action in now_state.legal_actions()]
    for state in next_states:
        values, _ = max_n(state, depth-1)
        value = values[now_state.turn % 4]
        if value > best_val:
            best_val = value
            best_state = state
            best_vals = values

    return best_vals, best_state

def max_n_immediate_pruning(now_state: State, depth, upper_bound):
    now_state = copy.deepcopy(now_state)

    if depth == 0 or now_state.is_done():
        return huristic(state), now_state
    
    best_val = -float('inf')
    best_state = None
    best_vals = None

    next_states = [now_state.next(action) for action in now_state.legal_actions()]
    for state in next_states:
        values, _ = max_n_immediate_pruning(state, depth-1, upper_bound)
        value = values[now_state.turn]

        if value == upper_bound:
            return values, state

        if value > best_val:
            best_val = value
            best_state = state
            best_vals = values

    return best_vals, best_state

def max_n_pruning(now_state: State, depth, upper_bound, global_upper_bound):
    now_state = copy.deepcopy(now_state)

    if depth == 0 or now_state.is_done():
        return huristic(now_state), now_state
    
    # best_val = -float('inf')
    # best_state = None
    # best_vals = None

    
    next_states = [now_state.next(action) for action in now_state.legal_actions()]

    best_vals, _ = max_n_pruning(next_states[0], depth-1, global_upper_bound, global_upper_bound)
    best_val = best_vals[now_state.turn%4]
    best_state = next_states[0]

    for state in next_states[1:]:
        if best_val >= upper_bound:
            return best_vals, best_state
        
        values, _ = max_n_pruning(state, depth-1, global_upper_bound-best_val, global_upper_bound)
        value = values[now_state.turn%4]

        if value > best_val:
            best_val = value
            best_state = state
            best_vals = values

    return best_vals, best_state

def random_play(state: State):
    return random.choice([state.next(action) for action in state.legal_actions()])

def max_n_action(state: State):
    if state.turn < 16:
        depth = 12
    elif state.turn < 32:
        depth = 12
    else:
        depth = 12
    values, next_state = max_n_pruning(state, depth, upper_bound=1, global_upper_bound=1)

    return next_state

def person_play(state: State):
    print(f"legal actions: {state.legal_actions()}")

    action = int(input("action: "))

    return State(state.next(action))

def play(state: State, player, time_list=None, p=True):
    state = copy.deepcopy(state)

    if len(state.legal_actions()) == 0:
        state.turn += 1
        return state

    start = time.time()
    next_state = player(state, p)
    end = time.time()
    print(f"turn: {state.turn}, player: {player}, runtime: {(end-start):.5f}", end='\r')

    run_time = end - start
    if time_list is not None:
        time_list.append(run_time)
    
    return next_state

if __name__ == "__main__":
    # now_state= State()

    # print(str(now_state), end='')
    # print("------------------------------------")
    time_list = []
    r = 100
    actions = [random_play, random_play, random_play, max_n_action]
    actions = [[action, 0] for action in actions]
    draws = 0
    for i in range(r):
        now_state= State()
        
        while(not now_state.is_done()):
            now_state = play(now_state, actions[0][0], p=False)
            if now_state.is_done():
                break

            now_state = play(now_state, actions[1][0], p=False)
            if now_state.is_done():
                break

            now_state = play(now_state, actions[2][0], p=False)
            if now_state.is_done():
                break

            now_state = play(now_state, actions[3][0], p=False)

        actions = actions[1:] + [actions[0]]
            
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
            actions[now_state.winner()][1] += 1
        else:
            draws += 1

        print(f"{i+1}/{r}: {actions[0][0]}: {actions[0][1]/r:.5f}, {actions[1][0]}: {actions[1][1]/r:.5f}, {actions[2][0]}: {actions[2][1]/r:.5f}, {actions[3][0]}: {actions[3][1]/r:.5f}, draw: {draws/r:.5f}", end='\n', flush=True)