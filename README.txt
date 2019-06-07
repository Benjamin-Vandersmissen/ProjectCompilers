The compiler can be used by the build.sh file. In the commandline you execute the sh and add as only argument the C file you wish to Compile.
If you wish to use the c2llvm or c2mips python scripts you can use them the same way, but with python3 instead of the exectuable sh file. If you also want an llvm file while using the c2mips python script, add as second argument "true" (without quotes). This will tell the script to write the llvm to a file too. This also indicates that the c2mips python script uses llvm to go from C to mips. 

Tests can be compiled by the test.sh file.

Implemnted optional requirements:
- constant folding
- warnings for always false/true conditions -> skipping unreachable code
- skip unused expressions
- in global scope, only take last constant declaration for a variable
- error if no return statement is given in non-void function
- conversion of types + warnings
- pointer operations (which are allowed in C, examples in the test_llvm file)
- char array assignment to a string


tests:
All tests can be found in the tests folder. The name of the test says what it will test and in the testfile more explanation is given.