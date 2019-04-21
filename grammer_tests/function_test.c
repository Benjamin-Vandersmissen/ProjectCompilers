#include <stdio.h>

int f();

char f2(){
    return 'c';
}

float f3( int a ){
    return 0.0;
}

void f4( int a, int b) {

}

int f(){
    return 1;
}

int main(){
    int x = 0;

    int a = f(x);

    int b = f(f(x));

    int c = f(a+b);

    int d = f();

    int e = f(5) + 99*f(6);

    int f = f(a*b);

    int g = f(55);

    int h = f(9, 9, 8, 7, 6);

    return 0;
}

#include <stdio.h>
