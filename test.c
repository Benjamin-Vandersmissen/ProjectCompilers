#include <stdio.h>
int a = 0;
int b = 10;
float c = 0.1;

//int fibo(int count){
//    if (count < 0){
//        char error[] = "Index needs to be higher than 0";
//        printf(error);
//        return -1;
//    }
//    if (count == 1)
//        return 1;
//    if (count == 2)
//        return 1;
//    return fibo(count-1) + fibo(count-2);
//}

char test[] = "fibo(%i)"; // %i

int f(int a){
    printf(test, a);
    return 0;
}

float main(){
//    int count = 3;
//    float a = 0;
//    a = 0.5;
////    int retvalue = fibo(count);
////    if (retvalue == -1)
////        return 1;
//    printf(test, count);
float a = 0.3;
int b = a;
return 0.5;
}
