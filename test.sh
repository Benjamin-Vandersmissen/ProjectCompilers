#!/bin/bash
java -jar antlr-4.7.2-complete.jar -Dlanguage=Python3 smallC.g4 -visitor
for filename in tests/*.c
do
    echo "\n\nStarting: $filename \n"

    if ["$filename" = "test_llvm.c"]
    then
        python3 c2llvm.py "$filename"
    elif ["$filename" = "test_mips.c"]
    then
        python3 c2mips.py "$filename"
    else
        python3 c2mips.py "$filename" true
    fi

    dot -Tpng "${filename%.*}.dot" -o "${filename%.*}.png"
done