// Test different pointer operations

#include <stdio.h>

char text[] = "Should be %i: %i\n";

int number = 17536;
int* globalPointer = &number;

int main() {
    int* pointer = &number;

    printf(text, 17536, *pointer);
    printf(text, 17536, *globalPointer);

    *pointer = 178;

    printf(text, 178, number);

    *globalPointer = 180;

    printf(text, 180, number);

    int depointer = *pointer;

    printf(text, 180, depointer);

    number = 1234;

    printf(text, 1234, *pointer);
    printf(text, 1234, *globalPointer);

    return 0;
}
