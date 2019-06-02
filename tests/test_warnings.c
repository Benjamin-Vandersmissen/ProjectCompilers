// Test if warnings are given at needed moments

int f(float* a){
    return 0;
}

int main(){  // warnings for conversions
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
    a = c;
    f = c;

    e[0] = e;

    f(c);
    return 0;
}