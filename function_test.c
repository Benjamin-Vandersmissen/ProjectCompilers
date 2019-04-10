#include <stdio.h>

int f();

char f2(){
    
}

float f3( int a ){

}

void f4( int a, int b) {

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
}

#include <stdio.h>
