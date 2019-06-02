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