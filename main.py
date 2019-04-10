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
    listener = customListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    parser.addParseListener(listener)

    file = open("AST.dot", "w")
    listener.AST.buildSymbolTable()
    listener.AST.toDot(file)


if __name__ == '__main__':
    main(sys.argv)
