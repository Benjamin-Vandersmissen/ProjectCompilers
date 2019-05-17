#include <stdio.h>

int alize = 29;

int main() {
    while  (alize > 6){
        char testLocalArray[] = {'y', 'o', 'u', ' ', 't', 'y', 'p', 'e', 'd', ':', 10, '%', 'f', 10, alize};
        printf(testLocalArray, alize);
        alize = alize - 1;
    }
    return alize;
}