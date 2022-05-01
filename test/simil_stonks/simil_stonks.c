#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int target = 0;

int buy_stonks() {
    char user_buf[300+1];
    printf("what is your api token?\n");
    scanf("%300s", user_buf);
    printf("buying stonks with token:\n");
    printf(user_buf);
}

int main(int argc, char *argv[])
{
    int resp;
    printf("welcome back to the trading app!\n\n");
    printf("what would you like to do?\n");
    printf("1) buy some stonks!\n");
    printf("2) view my portfolio\n");
    scanf("%d", &resp);

    if (resp == 1) {
        buy_stonks();
    } else if (resp == 2) {
        printf("Function not added\n");
    }

    printf("!!!!\n");
    if(target == 0xaa) {
        printf("Target modified correctly!\n");
    }

    printf("goodbye!\n");

    exit(0);
}