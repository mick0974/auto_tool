#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int target = 0;

int main(int argc, char **argv){

    char input[61];
    printf("Input: ");
    scanf("%60s", input);
    input[61] = '\0';

    char buffer[61];
    snprintf(buffer, sizeof buffer, input);
    buffer[sizeof (buffer) - 1] = 0;
    printf("Change i's value from 1 -> 500. ");

    if(target==0xcc0){
        printf("\nGOOD\n");
    } else {
        printf("No way...let me give you a hint!\n");
        printf("buffer : [%s] (%d)\n", buffer, strlen(buffer));
    }

    return 0;
}