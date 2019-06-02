// Test not generating useless code after return statement

int test(){
    if(0){
        return 10;
    }
    int a = 0;
    while(a){
        int b = 0;
        return 0;
        b = b + 1;
    }
    return 1;
    int b = 0;
    int c = 0;
    b = c * 20 + b;
}
