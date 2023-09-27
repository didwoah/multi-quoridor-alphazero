#include "main.h"

int bot2check[10][10];
int bot2stack[90][3];       //0==x //1==y //2==초기 방향

void bot2move() {
    memset(bot2check, 0, sizeof(bot2check));
    map[bot2.x][bot2.y] = 0;
    int rear = 0, front = 0;
    bot2check[bot2.x][bot2.y] = 1;
    for (int i = 0; i < 12; i++) {          //초기 방향 저장을 위해 12방향 먼저 bfs돌리고
        int nx = bot2.x + px[i];
        int ny = bot2.y + py[i];
        if (isRange(nx, ny)) {
            if (bot2check[nx][ny] == 0) {
                if (canGo(i, bot2.x, bot2.y, nx, ny)) {
                    bot2stack[rear][0] = nx;
                    bot2stack[rear][1] = ny;
                    bot2stack[rear++][2] = i;
                    bot2check[nx][ny] = 1;
                }
            }
        }
    }
    while (rear != front) {
        int x = bot2stack[front][0];
        int y = bot2stack[front][1];
        int w = bot2stack[front++][2];
        if (y == 9) {                           //먼저 도착하면 그 초기방향으로 움직인다
            bot2.x = bot2.x + px[w];
            bot2.y = bot2.y + py[w];
            break;
        }
        for (int i = 0; i < 12; i++) {
            int nx = x + px[i];
            int ny = y + py[i];
            if (isRange(nx, ny)) {
                if (bot2check[nx][ny] == 0) {
                    if (canGo(i, x, y, nx, ny)) {
                        bot2stack[rear][0] = nx;
                        bot2stack[rear][1] = ny;
                        bot2stack[rear++][2] = w;
                        bot2check[nx][ny] = 1;
                    }
                }
            }
        }
    }
    map[bot2.x][bot2.y] = 2;
}

void randomWalling(int depth) {
    srand(depth);
    int w = (rand() % 2) + 1;       //가로,세로 랜덤
    int x = (rand() % 8) + 1;
    int y = (rand() % 8) + 1;       //x,y좌표 1~8까지면 범위 벗어나지 않음!
    if (!crossWall(w, x, y)) {
        switch (w) {
        case garo:
            garowall[x][y] = wallnum;
            garowall[x][y + 1] = wallnum++;
            if (dfs() != 0) {
                garowall[x][y] = 0;
                garowall[x][y + 1] = 0;
                wallnum--;
                randomWalling((depth + (rand() % 30000)) % 987654321);
            }
            break;
        case sero:
            serowall[x][y] = wallnum;
            serowall[x + 1][y] = wallnum++;
            if (dfs() != 0) {
                serowall[x][y] = 0;
                serowall[x + 1][y] = 0;
                wallnum--;
                randomWalling((depth + (rand() % 30000)) % 987654321);
            }
            break;
        }
    }
    else {
        randomWalling((depth + (rand() % 30000)) % 987654321);
    }
}

void bot2playing() {                //벽 모두 랜덤으로 설치하고 최단 경로로 가는 AI
    if (bot2.canwall != 0) {
        bot2.canwall--;
        srand(time(NULL));
        randomWalling(rand()%1000);
    }
    else bot2move();
    printf("bot2이 플레이 후\n");
    print();
}