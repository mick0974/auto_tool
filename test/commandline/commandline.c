#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int target = 0;

int main(int argc, char **argv)
{
    char *string1 = malloc(300*sizeof(char));
    char string2[300];

    char a[] = "DDDD";

    printf("Input 1:\n");
    printf("L'input è: ");
    printf(argv[1]);
    printf("Input 2:\n");
    printf(argv[2]);
    printf("\n");

    printf("Il valore di target è %i\n", target);

    if (target == 1)
        printf("VINTO\n");

    printf("Indirizzo a run-time di target: %p\n", &target);

    return 0;
}