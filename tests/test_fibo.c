#include <stdio.h>
int a = 0;
int b = 10;
float c = 0.1;

int fibo(int count){
    if (count == 1)
        return 1;
    if (count == 2)
        return 1;
    return fibo(count-1) + fibo(count-2);
}
int main(){

    int test[] = {37, 105, 0};

    int count = 15;
    int retvalue = fibo(count);
    printf(test, retvalue);
return 0;
}
