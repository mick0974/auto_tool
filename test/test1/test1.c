#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int twentythree = 0x6050;

int main(int argc, char* argv[]) {
   if(argc < 6){
      printf("I want more inputs!\n");
      return 0;
   }
   
   int sum = 0, i = 0;
   while(i < (argc - 1)) sum += atoi(argv[++i]);
   
   if(sum < 100){
      printf("I want bigger numbers!\n");
      return 0;
   }
   
   char number[50];
   printf("Insert a number: ");
   scanf("%50s", number);

   printf("The inserted value is ");
   printf(number);
   
   printf("\n");
   
   if(twentythree == 0x602030){
      printf("Ok\n");
   }
   
   return 0;
}
