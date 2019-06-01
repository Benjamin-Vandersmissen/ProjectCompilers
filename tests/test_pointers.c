#include <stdio.h>

char text[] = "Should be %i: %i\n";

int number = 17536;

int main() {
    int* pointer = &number;

    printf(text, 17536, *pointer);

    *pointer = 178;

    int depointer = *pointer;

    printf(text, 178, depointer);

    return 0;
}
