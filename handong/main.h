#pragma warning (disable: 4996)
#define _CRT_NO_SECURE_WARNINGS
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<math.h>
#include <time.h>

#define MOD 987654321

typedef struct Position {   //x,y좌표,설치가능한 벽개수
    int x, y, canwall;
}position;

extern position player;
extern position bot1;
extern position bot2;
extern position bot3;

extern int firstattck;
extern int playerscore, bot1score, bot2score, bot3score;
extern int wallnum;
extern int map[10][10];
extern int serowall[10][9];
extern int garowall[9][10];
extern int px[12];
extern int py[12];
extern int que[90][2];

void Start();
void print();
void playermove(); 
void removeWall();
void Play();
void walling();
void move();
void bot1move();
void bot2move();
void bot2playing();
void bot3move();

bool isRange(int x, int y);
bool wallIsRange(int x, int y);
bool canGo(int dir, int x, int y, int nx, int ny);
bool crossWall(int type, int startx, int starty);

int win();
int dfs();

enum Direction {
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
};

enum Wall {
    garo = 1,
    sero = 2
};