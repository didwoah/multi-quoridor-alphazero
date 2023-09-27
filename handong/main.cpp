#include "main.h"

position player;
position bot1;
position bot2;
position bot3;

int map[10][10];      //1==봇1   //2==봇2  //3==봇3  //4==player
int serowall[10][9];        //세로 벽
int garowall[9][10];        //가로 벽
int px[12] = { 1,0,-1,0,1,1,-1,-1,2,0,-2,0 };   //상하좌우 4대각(3,1,9,7) 2칸씩 상하좌우
int py[12] = { 0,1,0,-1,1,-1,1,-1,0,2,0,-2 };   
int que[90][2];                                 //dfs돌릴 큐
int firstattck;                                 //선공 정하는 변수
int playerscore, bot1score, bot2score, bot3score;       //각각 점수
int wallnum;                                            //벽에 넘버 지정해서 교차안되게 만듬

int main() {
    firstattck = 1;
    Play();
}