// Test if the compiler kan compile a fibonacci number program

#include <stdio.h>
int a = 0;
int b = 10;
float c = 0.1;

int fibo(int count){
    if (count < 0){
        char error[] = "Index needs to be higher than 0";
        printf(error);
        return -1;
    }
    if (count == 1)
        return 1;
    if (count == 2)
        return 1;
    return fibo(count-1) + fibo(count-2);
}


int main(){

    char inp[] = "%i";

    char test[] = "fibo(%i) = %i";

    int count = 3;
    scanf(inp, &count);
    int retvalue = fibo(count);
    if (retvalue == -1)
        return 1;
    printf(test, count, retvalue);
return 0;
}
