#include <stdio.h>

char text[] = "Should be %i: %i\n";

int a = 123;
int * a1 = &a;

int main(){
    a = 1234;
    printf(text, 1234, *a1);
    return 0;
}