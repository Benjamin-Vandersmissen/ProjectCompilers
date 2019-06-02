#!/bin/bash
java -jar antlr-4.7.2-complete.jar -Dlanguage=Python3 smallC.g4 -visitor
for filename in tests/*.c
do
    printf "\n\n(bash) Starting: $filename \n"

    if [ "$filename" == "tests/test_llvm.c" ]; then
        python3 c2llvm.py "$filename"
    elif [ "$filename" == "tests/test_mips.c" ]; then
        python3 c2mips.py "$filename"
    else
        python3 c2mips.py "$filename" true
    fi

    printf "(bash) Making image of dot...\n"
    dot -Tpng "${filename%.*}.dot" -o "${filename%.*}.png"

    printf "(bash) End $filename"
done