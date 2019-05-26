#include <stdio.h>
int a = 0;
int b = 10;
float c = 0.1;

int fibo(float count){
    if (count == 1.0)
        return 1;
    if (count == 2.0)
        return 1;
    return fibo(count-1) + fibo(count-2);
}

int test[] = {37, 105, 0}; // %i

int main(){

    float count = 3;

//    int a =1;
//    int b = 2;
//    int c = 3;
//    int d = 4;
//    int e = 5;
//    int f = (a-b)+(c+d)*e;

    int retvalue = fibo(count);
    printf(test, retvalue);
return 0;
}
