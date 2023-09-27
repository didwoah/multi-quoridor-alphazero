from enum import Enum
import copy
from collections import deque
import random


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


class Wall(Enum):
    garo = 1,
    sero = 2,


dr = [1, 0, -1, 0, 1, 1, -1, -1, 2, 0, -2, 0]
dc = [0, 1, 0, -1, 1, -1, 1, -1, 0, 2, 0, -2]
# player = [player0, player1, player2, player 3]
# player = (r, c, horizontalwall, verticalwall)
# Endpoint 0 : r=0, 1: r=8, 2: c=8, 3: c=0
# 0~7 말 8~71 horizontal 72~135 vertical
# 처음 turn 0 ㅋ

player_info = [[8, 4, [], []], [0, 4, [], []], [4, 0, [], []], [4, 8, [], []]]


class State:
    def __init__(self, player=player_info, turn=None):
        # turn 0, 1, 2, 3
        # none일 경우 없다고 가정
        self.player = player
        self.turn = turn if turn != None else 0
        self.wallcnt = 0  # 필요함.. 교차되는 것 검증할때 벽 num
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.serowall = [[0 for _ in range(8)] for _ in range(9)]
        self.garowall = [[0 for _ in range(9)] for _ in range(8)]

        for i, p in enumerate(player):
            self.board[p[0]][p[1]] = i + 1

            for h in p[2]:
                self.wallcnt += 1
                self.garowall[h[0]][h[1]] = self.wallcnt
                self.garowall[h[0]][h[1]+1] = self.wallcnt

            for v in p[3]:
                self.wallcnt += 1
                self.serowall[v[0]][v[1]] = self.wallcnt
                self.serowall[v[0]+1][v[1]] = self.wallcnt

    def is_draw(self):
        return self.turn > 100

    def left_wall(self):
        count = len(self.player[self.turn % 4][2]) + \
            len(self.player[self.turn % 4][3])
        return 5 - count

    def is_range(self, r, c):
        if r < 0 or r > 8 or c < 0 or c > 8:
            return False
        return True

    def wall_is_range(self, r, c):
        if r < 0 or r > 7 or c < 0 or c > 7:
            return False
        return True

    def winner(self, turn=None):
        turn = self.turn % 4 if turn == None else turn
        if turn == 0 and self.player[turn][0] == 0:
            return 0
        elif turn == 1 and self.player[turn][0] == 8:
            return 1
        elif turn == 2 and self.player[turn][1] == 8:
            return 2
        elif turn == 3 and self.player[turn][1] == 0:
            return 3
        else:
            return -1

    def is_done(self, turn=None):
        turn = self.turn if turn == None else turn
        if (self.is_draw()):
            return 1
        else:
            return self.winner(turn) != -1

    def next(self, action):
        p = self.player[self.turn % 4]

        if (action < 4):
            if (self.can_go(action, p[0], p[1], p[0] + dr[action], p[1] + dc[action])):
                dir = action
            else:
                dir = action + 8
            p[0], p[1] = p[0] + dr[dir], p[1] + dc[dir]

        elif (action < 8):
            p[0], p[1] = p[0] + dr[action], p[1] + dc[action]

        elif (action < 72):
            r, c = self.number_to_coordinate(action, Wall.garo.value[0])
            p[2].append((r, c))

        elif (action < 136):
            r, c = self.number_to_coordinate(action, Wall.sero.value[0])
            p[3].append((r, c))

        self.turn += 1
        return State(self.player, self.turn)

    def legal_actions(self):
        actions = []
        r = self.player[self.turn % 4][0]
        c = self.player[self.turn % 4][1]

        for direction in range(12):
            nr = r + dr[direction]
            nc = c + dc[direction]
            if (self.is_range(nr, nc)):
                if (self.can_go(direction, r, c, nr, nc)):
                    if (direction > 7):
                        actions.append(direction-8)
                    else:
                        actions.append(direction)
        actions.sort()
        if (self.left_wall() <= 0):
            return actions
        for a in range(8, 136):
            if a < 72:
                type = 1
            elif a < 136:
                type = 2
            row, col = self.number_to_coordinate(a, type)
            if (self.walling(type, row, col)):
                actions.append(a)

        return actions

    def can_go(self, direction, r, c, nr, nc):
        if direction == Direction.Down.value[0]:
            if self.garowall[r][c] == 0 and self.board[nr][nc] == 0:
                return True
        elif direction == Direction.Right.value[0]:
            if self.serowall[r][c] == 0 and self.board[nr][nc] == 0:
                return True
        elif direction == Direction.Up.value[0]:
            if self.garowall[r - 1][c] == 0 and self.board[nr][nc] == 0:
                return True
        elif direction == Direction.Left.value[0]:
            if self.serowall[r][c - 1] == 0 and self.board[nr][nc] == 0:
                return True
        elif direction == Direction.DownRight.value[0]:
            if (
                self.garowall[r][c] == 0
                and self.board[r + 1][c] != 0
                and ((r + 2 > 8) or self.garowall[r + 1][c] != 0 or self.board[r + 2][c] != 0)
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
        elif direction == Direction.DownLeft.value[0]:
            if (
                self.garowall[r][c] == 0
                and self.board[r + 1][c] != 0
                and ((r + 2 > 8) or self.garowall[r + 1][c] != 0 or self.board[r + 2][c] != 0)
                and self.serowall[r + 1][c - 1] == 0
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
        elif direction == Direction.UpRight.value[0]:
            if (
                self.serowall[r][c] == 0
                and self.board[r][c + 1] != 0
                and (c + 2 > 8 or self.serowall[r][c + 1] != 0 or self.board[r][c + 2] != 0)
                and self.garowall[r - 1][c + 1] == 0
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
        elif direction == Direction.UpLeft.value[0]:
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
        elif direction == Direction.DownDown.value[0]:
            if (
                self.garowall[r][c] == 0
                and self.board[r + 1][c] != 0
                and self.garowall[r + 1][c] == 0
                and self.board[nr][nc] == 0
            ):
                return True
        elif direction == Direction.RightRight.value[0]:
            if (
                self.serowall[r][c] == 0
                and self.board[r][c + 1] != 0
                and self.serowall[r][c + 1] == 0
                and self.board[nr][nc] == 0
            ):
                return True
        elif direction == Direction.UpUp.value[0]:
            if (
                self.garowall[r - 1][c] == 0
                and self.board[r - 1][c] != 0
                and self.garowall[r - 2][c] == 0
                and self.board[nr][nc] == 0
            ):
                return True
        elif direction == Direction.LeftLeft.value[0]:
            if (
                self.serowall[r][c - 1] == 0
                and self.board[r][c - 1] != 0
                and self.serowall[r][c - 2] == 0
                and self.board[nr][nc] == 0
            ):
                return True

        return False

    def number_to_coordinate(self, number, type):
        if (type == Wall.garo.value[0]):
            number -= 8
        else:
            number -= 72
        row = number // 8
        col = number % 8
        return row, col

    def coordinate_to_number(self, row, col, type):
        number = row * 8 + col
        if (type == Wall.garo.value[0]):
            number += 8
        else:
            number += 72
        return number

    def canReachEnd(self, idx):
        if (self.is_done(idx)):
            return True

        que = deque()
        check = [[0 for _ in range(9)] for _ in range(9)]

        r, c = self.player[idx][0], self.player[idx][1]
        que.append((r, c))
        check[r][c] = 1

        while len(que):
            r, c = que.popleft()

            if idx == 0 and r == 0:
                return True
            elif idx == 1 and r == 8:
                return True
            elif idx == 2 and c == 8:
                return True
            elif idx == 3 and c == 0:
                return True

            for i in range(4):
                nr, nc = r + dr[i], c + dc[i]
                if self.is_range(nr, nc) and check[nr][nc] == 0:
                    if i == Direction.Down.value[0] and self.garowall[r][c] == 0:
                        check[nr][nc] = 1
                        que.append((nr, nc))
                    elif i == Direction.Right.value[0] and self.serowall[r][c] == 0:
                        check[nr][nc] = 1
                        que.append((nr, nc))
                    elif i == Direction.Up.value[0] and self.garowall[r - 1][c] == 0:
                        check[nr][nc] = 1
                        que.append((nr, nc))
                    elif i == Direction.Left.value[0] and self.serowall[r][c - 1] == 0:
                        check[nr][nc] = 1
                        que.append((nr, nc))

        return False

    def closed_bfs(self):
        for i, p in enumerate(self.player):
            if not self.canReachEnd(i):
                return True
        return False

    def crossWall(self, type, startx, starty):
        if type == Wall.garo.value[0]:
            if self.garowall[startx][starty] == 0 and self.garowall[startx][starty + 1] == 0:
                up = self.serowall[startx][starty]
                down = self.serowall[startx + 1][starty]
                if (up == 0 and down == 0) or up != down:
                    return False
            return True
        elif type == Wall.sero.value[0]:
            if self.serowall[startx][starty] == 0 and self.serowall[startx + 1][starty] == 0:
                left = self.garowall[startx][starty]
                right = self.garowall[startx][starty + 1]
                if (left == 0 and right == 0) or left != right:
                    return False
            return True

    def walling(self, type, startx, starty):
        if self.wall_is_range(startx, starty):
            if not self.crossWall(type, startx, starty):
                if type == Wall.garo.value[0]:
                    self.wallcnt += 1
                    self.garowall[startx][starty] = self.wallcnt
                    self.garowall[startx][starty + 1] = self.wallcnt

                    if self.closed_bfs():
                        ret = False
                    else:
                        ret = True
                    self.garowall[startx][starty] = 0
                    self.garowall[startx][starty + 1] = 0
                    self.wallcnt -= 1
                    return ret

                elif type == Wall.sero.value[0]:
                    self.wallcnt += 1
                    self.serowall[startx][starty] = self.wallcnt
                    self.serowall[startx + 1][starty] = self.wallcnt

                    if self.closed_bfs():
                        ret = False
                    else:
                        ret = True
                    self.serowall[startx][starty] = 0
                    self.serowall[startx + 1][starty] = 0
                    self.wallcnt -= 1
                    return ret
            else:
                return False
        else:
            return False

    def __str__(self):
        result = ""

        for i in range(8):
            for j in range(8):
                result += str(self.board[i][j])
                if self.serowall[i][j] == 0:
                    result += " "
                else:
                    result += "|"
            result += str(self.board[i][8]) + "\n"

            for j in range(8):
                if self.garowall[i][j] == 0:
                    result += "  "
                else:
                    result += "- "
            result += "\n"

        for j in range(8):
            result += str(self.board[8][j])
            if self.serowall[8][j] == 0:
                result += " "
            else:
                result += "|"
        result += str(self.board[8][8]) + "\n\n"

        return result


def random_action(state):
    legal_actions = state.legal_actions()
    return legal_actions[random.randint(0, len(legal_actions)-1)]


# State 클래스를 사용하여 게임 상태 초기화

state = State()
# state = state.next(11)
# print(state)
# state = state.next(74)
# print(state)
# r,c = state.number_to_coordinate(76,2)
# if(state.walling(2,r,c)):
#     state = state.next(76)
# print(state)


while True:
    if state.is_done():
        break

    action = random_action(state)

    state = state.next(action)

    print(state)
    print()
