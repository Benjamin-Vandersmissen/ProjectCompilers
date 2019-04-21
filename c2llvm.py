import sys

from antlr4 import *

from customListener import customListener
from smallCLexer import smallCLexer
from smallCParser import smallCParser


def main(argv):
    filename = argv[1][0:-2]

    # parse the given c file
    text = FileStream(argv[1])
    lexer = smallCLexer(text)
    stream = CommonTokenStream(lexer)
    parser = smallCParser(stream)
    tree = parser.program()
    if parser._syntaxErrors > 0:
        exit(1)

    # create the AST
    listener = customListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    parser.addParseListener(listener)

    # print the AST to a dot file
    dotFile = open(filename + ".dot", "w")
    listener.AST.buildSymbolTable()
    listener.AST.toDot(dotFile)
    dotFile.close()

    # create the llvm code
    llvmFile = open(filename + ".ll", "w+")
    listener.AST.toLLVM(llvmFile)
    llvmFile.close()

if __name__ == '__main__':
    main(sys.argv)
