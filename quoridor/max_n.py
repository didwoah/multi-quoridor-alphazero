import copy

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

def max_n_pruning(now_state, depth, upper_bound, global_upper_bound):
    now_state = copy.deepcopy(now_state)

    if depth == 0 or now_state.is_end():
        return now_state.evaluate(), now_state
    
    # best_val = -float('inf')
    # best_state = None
    # best_vals = None

    next_states = now_state.generate_states()

    best_vals, _ = max_n_pruning(next_states[0], depth-1, global_upper_bound, global_upper_bound)
    best_state = next_states[0]
    best_val = best_vals[now_state.turn]

    for state in next_states[1:]:
        if best_val >= upper_bound:
            return best_vals, best_state
        
        values, _ = max_n_pruning(state, depth-1, global_upper_bound-best_val, global_upper_bound)
        value = values[now_state.turn]

        if value > best_val:
            best_val = value
            best_state = state
            best_vals = values

    return best_vals, best_state
