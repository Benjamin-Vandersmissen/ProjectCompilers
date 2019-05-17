#include <stdio.h>
int b = 45;
char d = 128;
char f = 12.03;
float g = 12.0897;

float testDec(float f, char c, int i, float* f1, int* i1, char** c2){
    return *f1;
}

/// test if, else, while, functioncall, return
int main(){
    int a = 1 + 'A' + 2.01;
    int x = 1 + a + 3 + 7;
    char e = 'A';
    float i = testDec(g, d, a, &g, &a, &d);
    {
        e = a;
        char a = 12;
        e = a;
    }
    e = a;  // a should be local int
    if (e == d){
        if (a) {
            a = 0;
            return a;
        }
        else a = 1;
        if (1){
            if(0){
                return 555555;
            }
        }
    }
    else {
        while(a > b){
            a = a + f;
            while (a < f * 2) a = a - f;
            if (a < 0) a = 0;
            else {
                char testLocalArray[] = {'y', 'o', 'u', ' ', 't', 'y', 'p', 'e', 'd', ':', 10, '%', 'f', 10, 0};
                int* testLocalEmptyArray[2];
                float testLocalArrayToShort[4] = {1,2};
//                int testExpressionArray[a + b];  // TODO: optional?
                printf(testLocalArray, a);
                if (a == 0) return a;
                else return a = 0;
            }
        }
    }
    int* a1 = &a + 7;
    a1 = &a - e;
    return *a1 + 12 * a;
}