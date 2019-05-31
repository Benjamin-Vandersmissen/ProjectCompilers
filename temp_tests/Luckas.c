#include <stdio.h>

int number = 17536;

int main() {
    int* pointer = &number;

    *pointer = 10;

    int depointer = *pointer;

    char a[] = "%i\n";
    printf(a, depointer);

    return 0;
}