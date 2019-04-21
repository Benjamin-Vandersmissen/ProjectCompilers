int a[2] = {1,2};

void test(int x){
int b[] = {1,x};
}

void test2(){
int b[] = {25, 35};
}

//@X = global i32 17
//@Y = global i32 42
//@Z = global [2 x i32*] [ i32* @X, i32* @Y ]

int main(){
int a[2];
a[1];
a[2];
return a[1];
}

//define i32 @main() #0 {
//  %1 = alloca [13 x i32], align 16
//  %2 = getelementptr inbounds [13 x i32], [13 x i32]* %1, i64 0, i64 1
//  %3 = load i32, i32* %2, align 4
//  %4 = getelementptr inbounds [13 x i32], [13 x i32]* %1, i64 0, i64 2
//  %5 = load i32, i32* %4, align 8
//  ret i32 0
//}