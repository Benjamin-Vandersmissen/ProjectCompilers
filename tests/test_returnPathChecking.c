// Test the return from non-void function error

int f1(){
    return 0;
}

int f2(){
    int a = 0;
    if(a){
        return 0;
    }
    else{
        return 1;
    }
}

int f3(){
    int a = 0;
    if (a){
        int a = 0;
        while(a){
            return a;
        }
        return 0;
    }
    else{
        return 1;
    }
}

void f4(){

}

// should fail
int f5(){

}

// should fail
int f6(){
    int a = 0;
    if (a){
        return 0;

    }
}

// should fail
int f7(){
    int a = 0;
    while(a){
        return 0;
    }
}
