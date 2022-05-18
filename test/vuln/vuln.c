#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <wchar.h>
#include <locale.h>

int target = 0xaf;

void vuln(){
   char story[128];

   printf("Tell me a story and then I'll tell you one >> ");
   scanf("%127s", story);
   printf("Here's a story - \n");
   printf(story);
   printf("\n");
}

int main(int argc, char **argv){
  vuln();

  if(target == 0xffffffff) {
    printf("Target modified correctly!\n");
  }

  return 0;
}
