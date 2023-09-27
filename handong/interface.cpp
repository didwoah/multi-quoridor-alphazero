#include "main.h"

void reset() {      //점수 출력 후 map에서 위치 제거
    printf("player : %d bot1 : %d bot2 : %d bot3 : %d\n", playerscore, bot1score, bot2score, bot3score);
    map[player.x][player.y] = 0;
    map[bot1.x][bot1.y] = 0;
    map[bot2.x][bot2.y] = 0;
    map[bot3.x][bot3.y] = 0;
}

int win() {      //누가 이겼는지 체크               //봇1 위쪽시작 //봇2 왼쪽시작 //봇3 오른쪽시작
    if (player.x == 1) {
        printf("player가 이겼습니다.\n");
        playerscore++;
        return 1;
    }
    else if (bot1.x == 9) {
        printf("bot1이 이겼습니다.\n");
        bot1score++;
        return 1;
    }
    else if (bot2.y == 9) {
        printf("bot2가 이겼습니다.\n");
        bot2score++;
        return 1;
    }
    else if (bot3.y == 1) {
        printf("bot3가 이겼습니다.\n");
        bot3score++;
        return 1;
    }
    else return 0;
}

void initSetting() {
    //초기 위치, 남은 벽개수 설정
    bot1 = { 1,5,5 };
    bot2 = { 5,1,5 };
    bot3 = { 5,9,5 };
    player = { 9,5,5 };
    //상대방과 인접시 뛰어넘기 위해 map에 위치 표시
    map[bot1.x][bot1.y] = 1;
    map[bot2.x][bot2.y] = 2;
    map[bot3.x][bot3.y] = 3;
    map[player.x][player.y] = 4;
    //벽 넘버 설정
    wallnum = 1;
    //새 게임시 벽 초기화
    removeWall();
}

void Start() {                                          //게임 계속 진행 할지?
    int keep_going;
    printf("게임을 시작할까요? (시작=0,그만=1)\n");
    scanf("%d", &keep_going);
    if (keep_going == 1) {
        printf("게임을 종료합니다.\n");
        exit(0);
    }
    initSetting();
}

void playermove() {                                     //player턴
    int playeract;
    printf("벽을 놓으려면 1번 말을 움직이려면 2번\n");
    scanf("%d", &playeract);
    if (playeract == 1 && player.canwall != 0) {        //플레이어가 벽을 놓는다&&플레이어가 놓을 수 있는 벽의 개수가 1개 이상이면
        player.canwall--;
        walling();
    }
    else if (playeract == 1) {                          //플레이어가 벽을 놓는다 했는데 벽이 없으면
        printf("남은 벽개수가 없으므로 말을 움직입니다.\n");
        move();
    }
    else move();
    printf("플레이어가 플레이 후\n");
    print();
}

void Play() {
    bot1score = 0;
    bot2score = 0;
    bot3score = 0;
    playerscore = 0;
    while (firstattck++) {
        Start();
        while (1) {
            if (firstattck % 4 == 2) {   //player가 선공일때
                playermove();
                if (win() == 1) break;
                bot1move();
                if (win() == 1) break;
                bot2playing();
                if (win() == 1) break;
                bot3move();
                if (win() == 1) break;
            }
            else if(firstattck%4==3) {                  //bot1선공
                bot1move();
                if (win() == 1) break;
                bot2playing();
                if (win() == 1) break;
                bot3move();
                if (win() == 1) break;
                playermove();
                if (win() == 1) break;
            }
            else if (firstattck % 4 == 0) {             //bot2선공
                bot2playing();
                if (win() == 1) break;
                bot3move();
                if (win() == 1) break;
                playermove();
                if (win() == 1) break;
                bot1move();
                if (win() == 1) break;
            }
            else{                                        //bot3선공
                bot3move();
                if (win() == 1) break;
                playermove();
                if (win() == 1) break;
                bot1move();
                if (win() == 1) break;
                bot2playing();
                if (win() == 1) break;
            }
        }
        reset();
    }
}