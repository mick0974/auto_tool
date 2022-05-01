#include <stdio.h>
#include <unistd.h>

int secret_num = 0x0;

int main() {
    char trash[] = "AAAAAAAA";
    char name[64] = {0};
    char trash2[] = "AAAAAAAA";
    read(0, name, 64);
    printf("Ciao ");
    char trash3[] = "AAAAAAAA";
    printf(name);

    if(secret_num == 0xa) {
        printf("Hai assegnato il numero corretto al numero segreto\n");
    }
    return 0;
}