#!/bin/sh
java -jar antlr-4.7.2-complete.jar -Dlanguage=Python3 smallC.g4 -visitor
for filename in tests/*.c
do
    echo "\n\nTest: $filename"
    python3 c2mips.py "$filename" true

    dot -Tpng "${filename%.*}.dot" -o "${filename%.*}.png"
done