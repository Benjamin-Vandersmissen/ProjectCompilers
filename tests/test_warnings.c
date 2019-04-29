int f(float* a){

}

int main(){
    int a;
    float b;
    a = b;

    int* c;
    int ** d;
    int* e[2];
    float* f;

    c = d;
    d = c;
    d = e;
    c = a;
    f = c;

    e[0] = e;

    f(c);
    return 0;
}