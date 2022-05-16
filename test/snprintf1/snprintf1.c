#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv){
    int i = 1;
    printf("%p\n", &i);
    char buffer[64];

    //printf("Argv = %s\n", argv[1]);
    snprintf(buffer, sizeof buffer, argv[1]);
    buffer[sizeof (buffer) - 1] = '\0';
    //printf("buffer = %s\n", buffer);
    printf("Change i's value from 1 -> 500. ");

    if(i==500){
        printf("GOOD\n");
    }

    printf("No way...let me give you a hint!\n");
    printf("buffer : [%s] (%d)\n", buffer, strlen(buffer));
    printf ("i = %d (%p)\n", i, &i);
    return 0;
}