// test typechecking for return statements


// should warn
char f1(){
    return 1;
}

// should warn
int f2(){
    return 1.0;
}

// should warn
int f3(){
    int* a;
    return a;
}

// should warn
int* f4(){
    return 0;
}

// should warn
int* f5(){
    float* a;
    return a;
}

// should throw error
int* f6(){
    return 1.0;
}

//should throw error
float f7(){
    int* a;
    return a;
}

//should throw error
void f8(){
    return 1;
}

//should throw error
int f9(){
    return;
}