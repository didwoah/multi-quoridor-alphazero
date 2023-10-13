from collections import deque
import copy

from game import Direction
from game import State

E = 1
# 7 1 5 1
# 14
# 7 13 9 13
# 1 13 1.8 13
# 28.8
# 
def huristic_1(state: State):
    c0 = left_way(state, 0)
    c1 = left_way(state, 1)
    c2 = left_way(state, 2)
    c3 = left_way(state, 3)

    total_c = c0 + c1 + c2 + c3

    c0 = (total_c - c0)/(c0+E)
    c1 = (total_c - c1)/(c1+E)
    c2 = (total_c - c2)/(c2+E)
    c3 = (total_c - c3)/(c3+E)

    lw0 = state.get_left_wall(0)
    lw1 = state.get_left_wall(1)
    lw2 = state.get_left_wall(2)
    lw3 = state.get_left_wall(3)

    lw0 = lw0 if lw0 >= 0 else 0
    lw1 = lw1 if lw1 >= 0 else 0
    lw2 = lw2 if lw2 >= 0 else 0
    lw3 = lw3 if lw3 >= 0 else 0

    total_wall = lw0 + lw1 + lw2 +lw3
    
    lw0 = lw0/(total_wall - lw0+E)
    lw1 = lw1/(total_wall - lw1+E)
    lw2 = lw2/(total_wall - lw2+E)
    lw3 = lw3/(total_wall - lw3+E)

    # m0 = lw0**c0 if lw0 > 1 else (lw0+E)**(-c0)
    # m1 = lw1**c1 if lw1 > 1 else (lw1+E)**(-c1)
    # m2 = lw2**c2 if lw2 > 1 else (lw2+E)**(-c2)
    # m3 = lw3**c3 if lw3 > 1 else (lw3+E)**(-c3)

    m0 = c0*lw0
    m1 = c1*lw1
    m2 = c2*lw2
    m3 = c3*lw3

    total_m = m0 + m1 + m2 + m3

    return m0 / total_m, m1 / total_m, m2 / total_m, m3 / total_m
    
def huristic_2(state: State):
    c0 = left_way(state, 0)
    c1 = left_way(state, 1)
    c2 = left_way(state, 2)
    c3 = left_way(state, 3)

    total_c = c0 + c1 + c2 + c3

    c0 = (total_c - c0)/c0
    c1 = (total_c - c1)/c1
    c2 = (total_c - c2)/c2
    c3 = (total_c - c3)/c3

    total_c = c0 + c1 + c2 + c3

    return c0 / total_c, c1 / total_c, c2 / total_c, c3 / total_c

def huristic_3(state: State):
    c0 = 8-state.player[0].r
    c1 = state.player[1].r
    c2 = state.player[2].c
    c3 = 8-state.player[3].c

    total_wall = state.get_left_wall(0) + \
        state.get_left_wall(1) + \
        state.get_left_wall(2) + \
        state.get_left_wall(3)
    
    lw0 = total_wall - state.player[0].left_wall
    lw1 = total_wall - state.player[1].left_wall
    lw2 = total_wall - state.player[2].left_wall
    lw3 = total_wall - state.player[3].left_wall

    # population = distance(state.player[0].p, state.player[1].p) + \
    # distance(state.player[0].p, state.player[2].p) + \
    # distance(state.player[0].p, state.player[3].p) + \
    # distance(state.player[1].p, state.player[2].p) + \
    # distance(state.player[1].p, state.player[3].p) + \
    # distance(state.player[2].p, state.player[3].p)

    m0 = (lw0+1)
    m1 = (lw1+1)
    m2 = (lw2+1)
    m3 = (lw3+1)

    e0 = c0/m0
    e1 = c1/m1
    e2 = c2/m2
    e3 = c3/m3

    total_e = e0 + e1 + e2 + e3

    return e0 / total_e, e1 / total_e, e2 / total_e, e3 / total_e
    
def huristic_4(state: State):
    c0 = 8-state.player[0][0]
    c1 = state.player[1][0]
    c2 = state.player[2][1]
    c3 = 8-state.player[3][1]

    e0 = c0
    e1 = c1
    e2 = c2
    e3 = c3

    total_e = e0 + e1 + e2 + e3
    total_e = total_e if total_e != 0 else 1

    return e0 / total_e, e1 / total_e, e2 / total_e, e3 / total_e

def huristic_5(state: State):
    state = copy.deepcopy(state)

    c0 = 81-left_way(state, 0)
    c1 = 81-left_way(state, 1)
    c2 = 81-left_way(state, 2)
    c3 = 81-left_way(state, 3)

    total_c = c0 + c1 + c2 + c3 + E

    return c0 / total_c, c1 / total_c, c2 / total_c, c3 / total_c

def distance(p1, p2):
    return ((p1.r-p2.r)**2 + (p1.c-p2.c)**2)**(1/2)

def left_way(state, idx):
    state = copy.deepcopy(state)
    
    dr = [1, 0, -1, 0, 1, 1, -1, -1, 2, 0, -2, 0]
    dc = [0, 1, 0, -1, 1, -1, 1, -1, 0, 2, 0, -2]

    que = deque()
    check = [[0 for _ in range(9)] for _ in range(9)]

    r, c = state.player[idx][0], state.player[idx][1]
    que.append((r, c))
    check[r][c] = 1

    while len(que):
        r, c = que.popleft()

        if (idx == 0 and r == 0) or \
            (idx == 1 and r == 8) or \
            (idx == 2 and c == 8) or \
            (idx == 3 and c == 0):
            return check[r][c] - 1

        for d in Direction:
            nr, nc = r + dr[d.value[0]], c + dc[d.value[0]]
            if state.is_range(nr, nc) and check[nr][nc] == 0:
                if state.can_go(d.value[0], r, c, nr, nc):
                    check[nr][nc] = check[r][c] + 1
                    que.append((nr, nc))

    return 81