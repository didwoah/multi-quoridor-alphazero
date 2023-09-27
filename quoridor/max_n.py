import copy
import time

import sys
sys.path.append("D:/Project/multi-quoridor-alphazero")

from QuoridorAPI import State
import quoridor.huristic_evaluation as huristic_evaluation


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
        return huristic_evaluation.huristic_4(self)
    
    def get_left_wall(self, turn):
        count = len(self.player[turn][2]) + \
            len(self.player[turn][3])
        return 5 - count
    

def max_n(now_state, depth):
    now_state = copy.deepcopy(now_state)

    if depth == 0 or now_state.is_end():
        return now_state.evaluate(), now_state
    
    best_val = -float('inf')
    best_state = None
    best_vals = None

    next_states = now_state.generate_states()
    for state in next_states:
        values, _ = max_n(state, depth-1)
        value = values[now_state.turn]
        if value > best_val:
            best_val = value
            best_state = state
            best_vals = values

    return best_vals, best_state

def max_n_immediate_pruning(now_state, depth, upper_bound):
    now_state = copy.deepcopy(now_state)

    if depth == 0 or now_state.is_end():
        return now_state.evaluate(), now_state
    
    best_val = -float('inf')
    best_state = None
    best_vals = None

    next_states = now_state.generate_states()
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

def max_n_pruning(now_state: MyState, depth, upper_bound, global_upper_bound):
    now_state = copy.deepcopy(now_state)

    if depth == 0 or now_state.is_done():
        return now_state.evaluate(), now_state
    
    # best_val = -float('inf')
    # best_state = None
    # best_vals = None

    next_states = now_state.generate_states()

    best_vals, _ = max_n_pruning(next_states[0], depth-1, global_upper_bound, global_upper_bound)
    best_state = next_states[0]
    best_val = best_vals[now_state.turn%4]

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

def bot_play(state: MyState):
    return max_n_pruning(state, 1, upper_bound=1, global_upper_bound=1)

def person_play(state: MyState):
    print(f"legal actions: {state.legal_actions()}")
    action = int(input("action: "))
    return MyState(state.next(action))

def play(state: MyState, is_person, time_list=[]):
    print(f"turn: {state.turn % 4}")
    if is_person:
        next_state = person_play(state)
    else:
        start = time.time()
        values, next_state = bot_play(state)
        end = time.time()

        run_time = end - start
        time_list.append(run_time)

        print(values)
        print(f"{run_time:.5f} sec")

    print(str(next_state), end='')
    print("------------------------------------")
    
    return next_state

if __name__ == "__main__":
    now_state = MyState()

    print(str(now_state), end='')
    print("------------------------------------")
    time_list = []
    while(not now_state.is_end()):
        now_state = play(now_state, False, time_list)
        if now_state.is_end():
            break

        now_state = play(now_state, False)
        if now_state.is_end():
            break

        now_state = play(now_state, False)
        if now_state.is_end():
            break

        now_state = play(now_state, True)
        
    sum = 0
    count = 0
    for t in time_list:
        print(f"{t:.5f}", end=' ')
        sum += t
        count += 1
    print(f"\nsum: {sum:.5f}, count: {count}")
    print(f"avg: {sum/count:.5f}")