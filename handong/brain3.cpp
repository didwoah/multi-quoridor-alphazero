#include "main.h"

int bot3check[10][10];
int bot3stack[90][3];       //0==x //1==y //2==초기 방향

void bot3moving() {
    memset(bot3check, 0, sizeof(bot3check));
    map[bot3.x][bot3.y] = 0;
    int rear = 0, front = 0;
    bot3check[bot3.x][bot3.y] = 1;
    for (int i = 0; i < 12; i++) {          //초기 방향 저장을 위해 12방향 먼저 bfs돌리고
        int nx = bot3.x + px[i];
        int ny = bot3.y + py[i];
        if (isRange(nx, ny)) {
            if (bot3check[nx][ny] == 0) {
                if (canGo(i, bot3.x, bot3.y, nx, ny)) {
                    bot3stack[rear][0] = nx;
                    bot3stack[rear][1] = ny;
                    bot3stack[rear++][2] = i;
                    bot3check[nx][ny] = 1;
                }
            }
        }
    }
    while (rear != front) {
        int x = bot3stack[front][0];
        int y = bot3stack[front][1];
        int w = bot3stack[front++][2];
        if (y == 1) {                           //먼저 도착하면 그 초기방향으로 움직인다
            bot3.x = bot3.x + px[w];
            bot3.y = bot3.y + py[w];
            break;
        }
        for (int i = 0; i < 12; i++) {
            int nx = x + px[i];
            int ny = y + py[i];
            if (isRange(nx, ny)) {
                if (bot3check[nx][ny] == 0) {
                    if (canGo(i, x, y, nx, ny)) {
                        bot3stack[rear][0] = nx;
                        bot3stack[rear][1] = ny;
                        bot3stack[rear++][2] = w;
                        bot3check[nx][ny] = 1;
                    }
                }
            }
        }
    }
    map[bot3.x][bot3.y] = 3;
}

int othercheck[10][10];
int otherstack[90][2];

int min_distance(int pivotx, int pivoty, int way, int destination) {
    memset(othercheck, 0, sizeof(othercheck));
    othercheck[pivotx][pivoty] = 1;
    int rear = 0, front = 0;
    otherstack[rear][0] = pivotx;
    otherstack[rear++][1] = pivoty;
    while (rear != front) {
        int x = otherstack[front][0];
        int y = otherstack[front++][1];
        if (way == 1 && x == destination) return (othercheck[x][y] % 100);
        else if (way == 2 && y == destination) return (othercheck[x][y] % 100);
        for (int i = 0; i < 12; i++) {
            int nx = x + px[i];
            int ny = y + py[i];
            if (isRange(nx, ny)) {
                if (othercheck[nx][ny] == 0) {
                    if (canGo(i, x, y, nx, ny)) {
                        otherstack[rear][0] = nx;
                        otherstack[rear++][1] = ny;
                        othercheck[nx][ny] = othercheck[x][y]+1;
                    }
                }
            }
        }
    }
}

int mean;
int imsiw, imsix, imsiy;

void is_good(int w,int x,int y) {
    int pivot = min_distance(player.x, player.y, 1, 1) + min_distance(bot1.x, bot1.y, 1, 9) + min_distance(bot2.x, bot2.y, 2, 9) - min_distance(bot3.x, bot3.y, 2, 1);
    if (pivot > mean) {
        mean = pivot;
        imsiw = w;
        imsix = x;
        imsiy = y;
    }
}

void bot3walling() {
    mean = min_distance(player.x, player.y, 1, 1) + min_distance(bot1.x, bot1.y, 1, 9) + min_distance(bot2.x, bot2.y, 2, 9) - min_distance(bot3.x, bot3.y, 2, 1);
    int temp = mean;
    for (int w = 1; w < 3; w++) {
        for (int i = 1; i < 9; i++) {
            for (int j = 1; j < 9; j++) {
                if (!crossWall(w, i, j)) {
                    if (w == 1) {
                        garowall[i][j] = wallnum;
                        garowall[i][j+1] = wallnum++;
                        if (dfs() == 0) {                       //놓을 수 있다면
                            is_good(1,i,j);
                        }
                        garowall[i][j] = 0;
                        garowall[i][j+1] = 0;
                        wallnum--;
                    }
                    else {
                        serowall[i][j] = wallnum;
                        serowall[i + 1][j] = wallnum++;
                        if (dfs() == 0) {                       //놓을 수 있다면
                            is_good(2,i,j);
                        }
                        serowall[i][j] = 0;
                        serowall[i + 1][j] = 0;
                        wallnum--;
                    }
                }
            }
        }
    }
    if (mean > temp) {
        if (imsiw == 1) {
            garowall[imsix][imsiy] = wallnum;
            garowall[imsix][imsiy+1] = wallnum++;
        }
        else {
            serowall[imsix][imsiy] = wallnum;
            serowall[imsix+1][imsiy] = wallnum++;
        }
    }
    else {                  //기댓값 변화 없을 때
        bot3.canwall++;
        bot3moving();
    }
}

void bot3move() {
    if (bot3.canwall != 0) {
        bot3.canwall--;
        bot3walling();
    }
    else bot3moving();
    printf("bot3이 플레이 후\n");
    print();
}