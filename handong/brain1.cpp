#include "main.h"

int bot1check[10][10];
int bot1stack[90][3];       //0==x //1==y //2==초기 방향

void bot1move() {                                   //벽 세우는 거 못하고 최단경로로만 가는 AI
    memset(bot1check, 0, sizeof(bot1check));
    map[bot1.x][bot1.y] = 0;
    int rear = 0, front = 0;
    bot1check[bot1.x][bot1.y] = 1;
    for (int i = 0; i < 12; i++) {          //초기 방향 저장을 위해 12방향 먼저 bfs돌리고
        int nx = bot1.x + px[i];
        int ny = bot1.y + py[i];
        if (isRange(nx, ny)) {
            if (bot1check[nx][ny] == 0) {
                if (canGo(i, bot1.x, bot1.y, nx, ny)) {
                    bot1stack[rear][0] = nx;
                    bot1stack[rear][1] = ny;
                    bot1stack[rear++][2] = i;
                    bot1check[nx][ny] = 1;
                }
            }
        }
    }
    while (rear != front) {
        int x = bot1stack[front][0];
        int y = bot1stack[front][1];
        int w = bot1stack[front++][2];
        if (x == 9) {                           //먼저 도착하면 그 초기방향으로 움직인다
            bot1.x = bot1.x + px[w];
            bot1.y = bot1.y + py[w];
            break;
        }
        for (int i = 0; i < 12; i++) {
            int nx = x + px[i];
            int ny = y + py[i];
            if (isRange(nx, ny)) {
                if (bot1check[nx][ny] == 0) {
                    if (canGo(i, x, y, nx, ny)) {
                        bot1stack[rear][0] = nx;
                        bot1stack[rear][1] = ny;
                        bot1stack[rear++][2] = w;
                        bot1check[nx][ny] = 1;
                    }
                }
            }
        }
    }
    map[bot1.x][bot1.y] = 1;
    printf("bot1이 플레이 후\n");
    print();
}