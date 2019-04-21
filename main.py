import sys

from antlr4 import *

from customListener import customListener
from smallCLexer import smallCLexer
from smallCParser import smallCParser


def main(argv):
    text = FileStream(argv[1])
    lexer = smallCLexer(text)
    stream = CommonTokenStream(lexer)
    parser = smallCParser(stream)
    tree = parser.program()
    if parser._syntaxErrors > 0:
        exit(1)
    listener = customListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    parser.addParseListener(listener)

    dotFile = open("AST.dot", "w")
    listener.AST.buildSymbolTable()
    listener.AST.toDot(dotFile)
    dotFile.close()

    llvmFile = open("program.ll", "w+")
    listener.AST.toLLVM(llvmFile)
    llvmFile.close()

if __name__ == '__main__':
    main(sys.argv)
