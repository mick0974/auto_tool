#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int i = 0;

int main(int argc, char **argv){
    if(argc >= 3) {
        char buffer[64];

        snprintf(buffer, sizeof buffer, argv[1]);
        buffer[sizeof (buffer) - 1] = 0;
        printf("Change i's value from 1 -> 500. ");

        if(i==0x7d9a22){
            printf("GOOD\n");
            return 0;
        }

        printf("No way...let me give you a hint!\n");
        printf("buffer : [%s] (%d)\n", buffer, strlen(buffer));
        printf ("i = %d (%p)\n", i, &i);

    }
    return 0;
}