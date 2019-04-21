#!/bin/sh
java -jar antlr-4.7.2-complete.jar -Dlanguage=Python3 smallC.g4 -visitor

if [ -z "$1" ]
then
      echo "\No c file was given!"
      exit 1
fi

python3 c2llvm.py "$1"

file = echo "$1" | cut -d '.c' -f 2

dot -Tpng "$file.dot" -O