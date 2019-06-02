// Test removal of unused expressions

void f(){
}

int main(){
    int a = 0;
    0+0; //should be removed in AST
    29*25-34+1; //should be removed in AST
    f(); //should not be removed in AST
    a = a; //should be removed in AST

    //TODO: optimise these unused expressions?
    a = a + 0;
    a = a - 0;
    a = a * 1;
    a = a / 1;

    return 0;
}