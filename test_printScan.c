#include <stdio.h>

int f(int a, int b){
    return a + b;
}


int main(){
    float a;
    char scan[] = {'%', 'f', 0};
    scanf(scan, &a);
    char test[] = {'y', 'o', 'u', ' ', 't', 'y', 'p', 'e', 'd', ':', 10, '%', 'f', 10, 0};
    printf(test, a);
    return 0;
}