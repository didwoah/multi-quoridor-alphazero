#include "main.h"

bool canGo(int dir, int x, int y, int nx, int ny) {
    switch (dir) {
    case Down:
        if (garowall[x][y] == 0 && map[nx][ny] == 0) {
            return true;
        }
        break;
    case Right:
        if (serowall[x][y] == 0 && map[nx][ny] == 0) {
            return true;
        }
        break;
    case Up:
        if (garowall[x - 1][y] == 0 && map[nx][ny] == 0) {
            return true;
        }
        break;
    case Left:
        if (serowall[x][y - 1] == 0 && map[nx][ny] == 0) {
            return true;
        }
        break;
    case DownRight:
        if (garowall[x][y] == 0 && map[x + 1][y] != 0 && ((x + 2 > 9) || garowall[x + 1][y] != 0 || map[x + 2][y] != 0) && serowall[x + 1][y] == 0 && map[nx][ny] == 0) {
            return true;
        }               //5->6->3
        else if (serowall[x][y] == 0 && map[x][y + 1] != 0 && (y + 2 > 9 || serowall[x][y + 1] != 0 || map[x][y + 2] != 0) && garowall[x][y + 1] == 0 && map[nx][ny] == 0) {
            return true;
        }
        break;
    case DownLeft:
        if (garowall[x][y] == 0 && map[x + 1][y] != 0 && ((x + 2 > 9) || garowall[x + 1][y] != 0 || map[x + 2][y] != 0) && serowall[x][y] == 0 && map[nx][ny] == 0) {
            return true;
        }               //5->4->1
        else if (serowall[x][y - 1] == 0 && map[x][y - 1] != 0 && (y - 2 < 1 || serowall[x][y - 2] != 0 || map[x][y - 2] != 0) && garowall[x][y - 1] == 0 && map[nx][ny] == 0) {
            return true;
        }
        break;
    case UpRight:
        if (serowall[x][y] == 0 && map[x][y + 1] != 0 && (y + 2 > 9 || serowall[x][y + 1] != 0 || map[x][y + 2] != 0) && garowall[x][y] == 0 && map[nx][ny] == 0) {
            return true;
        }               //5->8->9
        else if (garowall[x - 1][y] == 0 && map[x - 1][y] != 0 && (x - 2 < 1 || garowall[x - 2][y] != 0 || map[x - 2][y] != 0) && serowall[x - 1][y] == 0 && map[nx][ny] == 0) {
            return true;
        }
        break;
    case UpLeft:
        if (serowall[x][y - 1] == 0 && map[x][y - 1] != 0 && (y - 2 < 1 || serowall[x][y - 2] != 0 || map[x][y - 2] != 0) && garowall[x - 1][y - 1] == 0 && map[nx][ny] == 0) {
            return true;
        }               //5->8->7
        else if (garowall[x - 1][y] == 0 && map[x - 1][y] != 0 && (x - 2 < 1 || garowall[x - 2][y] != 0 || map[x - 2][y] != 0) && serowall[x - 1][y - 1] == 0 && map[nx][ny] == 0) {
            return true;
        }
        break;
    case DownDown:
        if (garowall[x][y] == 0 && map[x + 1][y] != 0 && garowall[x + 1][y] == 0 && map[nx][ny] == 0) {
            return true;
        }
        break;
    case RightRight:
        if (serowall[x][y] == 0 && map[x][y + 1] != 0 && serowall[x][y + 1] == 0 && map[nx][ny] == 0) {
            return true;
        }
        break;
    case UpUp:
        if (garowall[x - 1][y] == 0 && map[x - 1][y] != 0 && garowall[x - 2][y] == 0 && map[nx][ny] == 0) {
            return true;
        }
        break;
    case LeftLeft:
        if (serowall[x][y - 1] == 0 && map[x][y - 1] != 0 && serowall[x][y - 2] == 0 && map[nx][ny] == 0) {
            return true;
        }
        break;
    }
    return false;
}

void move() {                   //player말 움직이기
    int cango[12][2];           //갈 수 있는곳좌표들의 stack
    int rear = 0;
    for (int i = 0; i < 12; i++) {
        int nx = player.x + px[i];
        int ny = player.y + py[i];
        if (isRange(nx, ny)) {
            if (canGo(i, player.x, player.y, nx, ny)) {
                cango[rear][0] = nx;
                cango[rear++][1] = ny;
            }
        }
    }
    map[player.x][player.y] = 0;
    int way;
    printf("갈수있는 곳\n");
    for (int i = 0; i < rear; i++) {
        printf("%d : (%d,%d)\n", i + 1, cango[i][0], cango[i][1]);
    }
    printf("입력해주세요.\n");
    scanf("%d", &way);
    player.x = cango[way - 1][0];
    player.y = cango[way - 1][1];
    map[player.x][player.y] = 4;
}