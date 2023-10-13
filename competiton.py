import brain
import max_n
import mcts
import time
import copy
from game import State
time_list = []
r = 100
wc = [0, 0, 0, 0, 0]

def play(state: State, player, time_list=None, p=True):
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

actions = [brain.brain1, mcts.dirtfyPlay, brain.brain3, max_n.max_n_action]
for i in range(r):
    now_state= State()
    
    while(not now_state.is_end()):
        now_state = max_n.play(now_state, actions[0], p=False)
        if now_state.is_end():
            break

        now_state = max_n.play(now_state, actions[1], p=False)
        if now_state.is_end():
            break

        now_state = max_n.play(now_state, actions[2], p=False)
        if now_state.is_end():
            break

        now_state = max_n.play(now_state, actions[3], p=False)

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
        wc[now_state.winner()] += 1
    else:
        wc[4] += 1

    print(f"{i+1}/{r}: {wc[0]/r:.5f}, {wc[1]/r:.5f}, {wc[2]/r:.5f}, {wc[3]/r:.5f}, {wc[4]/r:.5f}", end='\r', flush=True)