import random
import math

class State:

    def __init__(self, pieces=None, enemy_pieces=None):
        self.pieces = pieces if pieces != None else [0]*9
        self.enemy_pieces = enemy_pieces if enemy_pieces != None else [0]*9

    def price_count(self, pieces):
        count=0
        for i in pieces:
            if i == 1:
                count += 1
            
        return count
    
    def is_lose(self):
        def is_comp(x, y, dx, dy):
            for k in range(3):
                if y < 0 or 2 < y or x < 0 or 2 < x or self.enemy_pieces[x + y * 3] == 0:
                    return False
                
                x = x + dx
                y = y + dy
            return True
        
        if is_comp(0, 0, 1, 1) or is_comp(0, 2, 1, -1):
            return True
        for i in range(3):
            if is_comp(0, i, 1, 0) or is_comp(i, 0, 0, 1):
                return True
        return False
    
    def is_draw(self):
        return self.price_count(self.pieces) + self.price_count(self.enemy_pieces) == 9
    
    def is_done(self):
        return self.is_lose() or self.is_draw()
    
    def next(self, action):
        pieces = self.pieces.copy()
        pieces[action] = 1
        return State(self.enemy_pieces, pieces)
    
    def legal_actions(self):
        actions = []
        for i in range(9):
            if self.pieces[i] == 0 and self.enemy_pieces[i] == 0:
                actions.append(i)
        return actions
    
    def is_first_player(self):
        return self.price_count(self.pieces) == self.price_count(self.enemy_pieces)
    
    def __str__(self):
        ox = ('o', 'x') if self.is_first_player() else ('x', 'o')
        str=''
        for i in range(9):
            if self.pieces[i] == 1:
                str += ox[0]
            elif self.enemy_pieces[i] == 1:
                str += ox[1]
            else:
                str += '-'
            if i % 3 == 2:
                str += '\n'
        return str
    
def random_action(state):
    legal_actions = state.legal_actions()
    return legal_actions[random.randint(0, len(legal_actions)-1)]

def alpha_beta(state, alpha, beta):

    if state.is_lose():
        return -1
    
    if state.is_draw():
        return 0
    
    for action in state.legal_actions():
        score = -alpha_beta(state.next(action), -beta, -alpha)
        if score > alpha:
            alpha = score

        if alpha >= beta:
            return alpha
        
    return alpha
    
def alpha_beta_action(state):
    best_action = 0
    alpha = -float('inf')
    str = ['', '']
    for action in state.legal_actions():
        score = -alpha_beta(state.next(action), -float('inf'), -alpha)
        if score > alpha:
            best_action = action
            alpha = score

        str[0] = '{}{:2d},'.format(str[0], action)
        str[1] = '{}{:2d},'.format(str[1], score)
    print('action:', str[0], '\nscore: ', str[1], '\n')

    return best_action

def playout(state):
    if state.is_lose():
        return -1
    
    if state.is_draw():
        return 0
    
    return -playout(state.next(random_action(state)))

def argmax(collection, key = None):
    return collection.index(max(collection))

def mcs_action(state):

    legal_actions = state.legal_actions()
    values = [0] * len(legal_actions)
    for i, action in enumerate(legal_actions):
        for _ in range(10):
            values[i] += -playout(state.next(action))

    return legal_actions[argmax(values)]

if __name__ == '__main__':

    state = State()

    while True:

        if state.is_done():
            break
        state = state.next(random_action(state))

        print(state)
        print()