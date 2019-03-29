import sys
from antlr4 import *
from smallCLexer import smallCLexer
from smallCParser import smallCParser
from smallCVisitor import smallCVisitor
from customListener import customListener

def main(argv):
    text = FileStream(argv[1])
    lexer = smallCLexer(text)
    stream = CommonTokenStream(lexer)
    parser = smallCParser(stream)
    tree = parser.program()
    file = open("AST.dot", "w+")
    file.write("digraph AST {\n")
    listener = customListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    parser.addParseListener(listener)
    file.write("\n}")
    
if __name__ == '__main__':
    main(sys.argv)
