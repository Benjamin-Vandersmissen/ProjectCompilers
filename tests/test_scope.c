// Test if the compiler can handle scopes, scopes in scopes, function scopes...

#include <stdio.h>

char text[] = "Should be %i: %i\n";

int a = 0;

void test(){
    printf(text, 0, a);
}

int main(){
    printf(text, 0, a);

    int a = 1;

    printf(text, 1, a);

    {
        printf(text, 1, a);

        int a = 2;

        printf(text, 2, a);
    }

    printf(text, 1, a);

    test();

    return 0;
}

// printf(text, , );