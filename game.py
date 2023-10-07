from enum import Enum
import copy
from collections import deque


class Direction(Enum):
    Down = 0,
    Right = 1,
    Up = 2,
    Left = 3,
    DownRight = 4,
    DownLeft = 5,
    UpRight = 6,
    UpLeft = 7,
    DownDown = 8,
    RightRight = 9,
    UpUp = 10,
    LeftLeft = 11,  

class Wall(Enum) :
    garo = 1,
    sero = 2

que = deque()

#player(r,c,hori[],verti[])
players = [(1,2,[(1,2),(2,4),(1,5)],[(1,3),(3,6)]),(1,2,[(1,2),(2,4),(1,5)],[(1,3),(3,6)]),
          (1,2,[(1,2),(2,4),(1,5)],[(1,3),(3,6)]),(1,2,[(1,2),(2,4),(1,5)],[(1,3),(3,6)])]

dr = [1,0,-1,0,1,1,-1,-1,2,0,-2,0]
dc = [0,1,0,-1,1,-1,1,-1,0,2,0,-2]
ddr = [1, 0, -1, 0]
ddc = [0, 1, 0, -1]
# player = [player0, player1, player2, player 3]
# player1 = (r, c, horizontalwall, verticalwall)
class State:
    def __init__(self, player, turn): 
        # turn 0, 1, 2, 3
        #none일 경우 없다고 가정
        self.player = player
        self.turn = turn

        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.serowall = [[0 for _ in range(8)] for _ in range(8)]
        self.garowall = [[0 for _ in range(8)] for _ in range(8)]

        for i,p in enumerate(player):
            if(self.turn == i):
                self.board[p[0]][p[1]] = 1 #?? player들 다 1로 기록해둠
            else:
                self.board[p[0]][p[1]] = -1 #?? player들 다 1로 기록해둠
            for h in p[2]:
                self.garowall[h[0]][h[1]] = 1
            for v in p[3]:
                self.serowall[v[0]][v[1]] = 1


    def left_wall(self, turn):
        count = 0
        for h in self.player[turn][2]:
            count+=1
        for v in self.player[turn][3]:
            count+=1
        return 5 - count
    
    def is_range(r, c):
        if r < 0 or r > 8 or c < 0 or c > 8:
            return False
        return True

    def wall_is_range(r, c):
        if r < 0 or r > 7 or c < 0 or c > 7:
            return False
        return True
    
    def winner(self):
        if self.turn == 0 and self.p[self.turn][0] == 0:
            return 0
        elif self.turn == 1 and self.p[self.turn][0] == 8:
            return 1
        elif self.turn == 2 and self.p[self.turn][1] == 8:
            return 2
        elif self.turn == 3 and self.p[self.turn][1] == 0:
            return 3
        else :
            return -1
        
    def is_done(self):
        return self.winner() != -1
    
    def next(self, action):
        return -1
    
    def legal_actions(self):
        actions = []
        r = self.player[self.turn][0]
        c = self.player[self.turn][1]
        
        for direction in range(12):
            nr = r + dr[direction]
            nc = c + dc[direction]
            if(self.is_range(nr,nc)):
                if(self.can_go(direction,r,c,nr,nc)):
                    if(direction > 7):
                        actions.append(direction-8)
                    else:
                        actions.append(direction)
        actions.sort()


        # 벽 둔다

        return actions
        
   
    def can_go(self, direction, r, c, nr, nc):
        if direction == "Down":
            if self.garowall[r][c] == 0 and self.board[nr][nc] == 0:
                return True
        elif direction == "Right":
            if self.serowall[r][c] == 0 and self.board[nr][nc] == 0:
                return True
        elif direction == "Up":
            if self.garowall[r - 1][c] == 0 and self.board[nr][nc] == 0:
                return True
        elif direction == "Left":
            if self.serowall[r][c - 1] == 0 and self.board[nr][nc] == 0:
                return True
        elif direction == "DownRight":
            if (
                self.garowall[r][c] == 0
                and self.board[r + 1][c] != 0
                and ((r + 2 > 8) or garowall[r + 1][c] != 0 or self.board[r + 2][c] != 0)
                and self.serowall[r + 1][c] == 0
                and self.board[nr][nc] == 0
             ):
                return True
            elif (
                self.serowall[r][c] == 0
                and self.board[r][c + 1] != 0
                and (c + 2 > 8 or self.serowall[r][c + 1] != 0 or self.board[r][c + 2] != 0)
                and self.garowall[r][c + 1] == 0
                and self.board[nr][nc] == 0
            ):
                return True
        elif direction == "DownLeft":
            if (
                self.garowall[r][c] == 0
                and self.board[r + 1][c] != 0
                and ((r + 2 > 8) or self.garowall[r + 1][c] != 0 or self.board[r + 2][c] != 0)
                and self.serowall[r][c] == 0
                and self.board[nr][nc] == 0
            ):
                return True
            elif (
                self.serowall[r][c - 1] == 0
                and self.board[r][c - 1] != 0
                and (c - 2 < 0 or self.serowall[r][c - 2] != 0 or self.board[r][c - 2] != 0)
                and self.garowall[r][c - 1] == 0
                and self.board[nr][nc] == 0
            ):
                return True
        elif direction == "UpRight":
            if (
                self.serowall[r][c] == 0
                and self.board[r][c + 1] != 0
                and (c + 2 > 8 or self.serowall[r][c + 1] != 0 or self.board[r][c + 2] != 0)
                and self.garowall[r][c] == 0
                and self.board[nr][nc] == 0
            ):
                return True
            elif (
                self.garowall[r - 1][c] == 0
                and self.board[r - 1][c] != 0
                and (r - 2 < 0 or self.garowall[r - 2][c] != 0 or self.board[r - 2][c] != 0)
                and self.serowall[r - 1][c] == 0
                and self.board[nr][nc] == 0
            ):
                return True
        elif direction == "UpLeft":
            if (
                self.serowall[r][c - 1] == 0
                and self.board[r][c - 1] != 0
                and (c - 2 < 0 or self.serowall[r][c - 2] != 0 or self.board[r][c - 2] != 0)
                and self.garowall[r - 1][c - 1] == 0
                and self.board[nr][nc] == 0
            ):
                return True
            elif (
                self.garowall[r - 1][c] == 0
                and self.board[r - 1][c] != 0
                and (r - 2 < 0 or self.garowall[r - 2][c] != 0 or self.board[r - 2][c] != 0)
                and self.serowall[r - 1][c - 1] == 0
                and self.board[nr][nc] == 0
            ):
                return True
        elif direction == "DownDown":
            if (
                self.garowall[r][c] == 0
                and self.board[r + 1][c] != 0
                and self.garowall[r + 1][c] == 0
                and self.board[nr][nc] == 0
            ):
                return True
        elif direction == "RightRight":
            if (
                self.serowall[r][c] == 0
                and self.board[r][c + 1] != 0
                and self.serowall[r][c + 1] == 0
                and self.board[nr][nc] == 0
            ):
                return True
        elif direction == "UpUp":
            if (
                self.garowall[r - 1][c] == 0
                and self.board[r - 1][c] != 0
                and self.garowall[r - 2][c] == 0
                and self.board[nr][nc] == 0
            ):
                return True
        elif direction == "LeftLeft":
            if (
                self.serowall[r][c - 1] == 0
                and self.board[r][c - 1] != 0
                and self.serowall[r][c - 2] == 0
                and self.board[nr][nc] == 0
            ):
                return True

        return False

    def number_to_coordinate(number,type):
        if(type == 'garo'):
            number -= 8
        else:
            number -= 72
        row = number // 8
        col = number % 8
        return row, col
    
    def coordinate_to_number(row, col, type):
        number = row * 8 + col
        if(type == 'garo'):
            number += 8
        else:
            number += 72
        return number