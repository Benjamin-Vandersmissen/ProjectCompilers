import sys

from antlr4 import *

from customListener import customListener
from smallCLexer import smallCLexer
from smallCParser import smallCParser
from LLVMTranspiler import LLVMTranspiler
from llvm import FileLookALike

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

    try:
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
    except Exception as e:
        print(e)
        exit(1)

    # create the llvm code
    if len(argv) == 3 and argv[2] == 'true':
        llvmFile = open(filename + ".ll", "w+")
        listener.AST.toLLVM(llvmFile)
        llvmFile.close()
        llvmFile = open(filename + '.ll', "r")
    else:
        llvmFile = FileLookALike()
        listener.AST.toLLVM(llvmFile)

    transpiler = LLVMTranspiler(filename, llvmFile)
    transpiler.transpile()

if __name__ == '__main__':
    main(sys.argv)
