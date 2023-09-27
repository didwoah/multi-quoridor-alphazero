from max_n import MyState

def huristic_1(state: MyState):
    c0 = 8-state.player[0][0]
    c1 = state.player[1][0]
    c2 = state.player[2][1]
    c3 = 8-state.player[3][1]

    total_wall = state.player[0].left_wall + \
        state.player[1].left_wall + \
        state.player[2].left_wall + \
        state.player[3].left_wall
    
    lw0 = total_wall - state.player[0].left_wall
    lw1 = total_wall - state.player[1].left_wall
    lw2 = total_wall - state.player[2].left_wall
    lw3 = total_wall - state.player[3].left_wall

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
    
def huristic_2(state: MyState):
    c0 = 8-state.player[0].r
    c1 = state.player[1].r
    c2 = state.player[2].c
    c3 = 8-state.player[3].c

    total_c = c0 + c1 + c2 + c3

    c0 /= total_c
    c1 /= total_c
    c2 /= total_c
    c3 /= total_c

    total_wall = state.player[0].left_wall + \
        state.player[1].left_wall + \
        state.player[2].left_wall + \
        state.player[3].left_wall
    
    lw0 = total_wall - state.player[0].left_wall
    lw1 = total_wall - state.player[1].left_wall
    lw2 = total_wall - state.player[2].left_wall
    lw3 = total_wall - state.player[3].left_wall

    m0 = (lw0+1)
    m1 = (lw1+1)
    m2 = (lw2+1)
    m3 = (lw3+1)

    e0 = c0*m0
    e1 = c1*m1
    e2 = c2*m2
    e3 = c3*m3

    total_e = e0 + e1 + e2 + e3

    return e0 / total_e, e1 / total_e, e2 / total_e, e3 / total_e

def huristic_3(state: MyState):
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
    
def huristic_4(state: MyState):
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
    

def distance(p1, p2):
    return ((p1.r-p2.r)**2 + (p1.c-p2.c)**2)**(1/2)