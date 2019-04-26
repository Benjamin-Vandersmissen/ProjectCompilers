//
// Created by laure on 16-Apr-19.
//

/// test include
#include <stdio.h>

/// test global declaration
int x1;
char x2;
float x3;

/// test global defenition
int a = 1 + 'A' + 2.01;  // should be 68
int b = 'A';  // should be 65
int c = 1.01;

char d = 1;
char e = 'A';
char f = 1.01;

float g = 1;
float h = 'A';
float i = 1.01;

/// test order of operators
int y = 3*8-3*(8+4)/1+12; // should be 0

//test global declaration with pointers
int* xx;
char*** xxx;
float**** xxxx;

/// test global defenitions with pointers
int* a1 = &a;
int** a12 = &a;
int* b1 = &d;
int* c1 = &g;

char* d1 = &b;
char* e1 = &e;
char* f1 = &h;

float* g1 = &c;
float* h1 = &f;
float* i1 = &i;

int ccc = 7;
char* d11 = 42 + &b - 10;
char* d12 = &b + 43 - (&ccc == &a1) + 53;

char testGlobalArray[] = {'y', 'o', 'u', ' ', 't', 'y', 'p', 'e', 'd', ':', 10, '%', 'f', 10, 0};
int* testGlobalEmptyArray[2];
int testGlobalArrayToShort[4] = {1,2};

/// test function declaration
float testDec(float, char, int, float*, int*, char**);

/// test not defined function
void shouldBeDeleted();

void globalPointerToLocalInt(){
    int a = *a1;
    int b = *d1;
    int c = *g1;

    char d = *b1;
    char e = *e1;
    char f = *h1;

    float g = *c1;
    float h = *f1;
    float i = *i1;

    float y = *a1 + f * *h1 * (14.04 + 5.96);
}

void globalIntToLocalPointer(){
    int* a1 = &a;
    int**** a2 = &a;
    int* b1 = &d;
    int* test = &d;
    int* c1 = &g;

    char* d1 = &b;
    char* e1 = &e;
    char* f1 = &h;

    float* g1 = &c;
    float* h1 = &f;
    float* i1 = &i;

    int ccc = 7;
    char* d11 = 42 + &b - 10;
    char* d12 = &b + 43 - (&ccc > &a1) + 53;
}

void alloctest(){
    /// test local declaration (standard 0)
    int x1;
    char x2;
    float x3;

    /// test local defenition
    int a = 1 + 'A' + 2.01;  // should be 68
    int b = 'A';  // should be 65
    int c = 1.01;

    char d = 1;
    char e = 'A';
    char f = 1.01;

    float g = 1;
    float h = 'A';
    float i = 1.01;

    /// test order of operators
    int y = 3*8-3*(8+4)/1+12; // should be 0

    ///test local declaration with pointers
    int* xx;
    char*** xxx;
    float**** xxxx;

    /// test local defenitions with pointers
    int* a1 = &a;
    int** a12 = &a;
    int* b1 = &d;
    int* c1 = &g;

    char* d1 = &b;
    char* e1 = &e;
    char* f1 = &h;

    float* g1 = &c;
    float* h1 = &f;
    float* i1 = &i;

    int ccc = 7;
    char* y11 = 42 + &b - 10;
    float* y12 = &b + 43 - (&ccc < &a1) + 53;

    ///test local defenitions with depointers
    int a2 = *a1;
    int b2 = *d1;
    int c2 = *g1;

    char d2 = *b1;
    char e2 = *e1;
    char f2 = *h1;

    float g2 = *c1;
    float h2 = *f1;
    float i2 = *i1;

    float y2 = *a1 + f * *h1 * (14.04 + 5.96);

    char testLocalArray[] = {'y', 'o', a, ' ', 't', 'y', 'p', 'e', 'd', ':', 10, '%', 'f', 10, 0};
    int* testLocalEmptyArray[2];
    float testLocalArrayToShort[4] = {1, *e1};
}

float testDec(float f, char c, int i, float* f1, int* i1, char** c2){
    int dit;
    float is;
    char geen;
    int* code = &dit;
    return *f1;
}

int f2(){
    return 0;
}

/// test if, else, while, functioncall, return
int main(){
    int a = 1 + 'A' + 2.01;
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

//int main(){
//    float k;
//    int j = 5;
//    j = 5+6*8;
//    {
//        int j = testDec(g, d, a, g1, d1, a1);
////        printf(j); // Moet 10 zijn
//    }
////    printf(j,j); // Moet 55 zijn - kan niet meer kloppen
//    j = j * j + j * (j + (j *3));
//    return j;
//}