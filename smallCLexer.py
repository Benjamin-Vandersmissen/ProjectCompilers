# Generated from smallC.g4 by ANTLR 4.6
from antlr4 import *
from io import StringIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\2\23")
        buf.write("_\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\3\2\3\2")
        buf.write("\3\3\3\3\3\4\3\4\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\6\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\13\3")
        buf.write("\13\3\f\3\f\3\r\3\r\3\16\6\16H\n\16\r\16\16\16I\3\17\3")
        buf.write("\17\3\20\6\20O\n\20\r\20\16\20P\3\20\3\20\3\21\3\21\3")
        buf.write("\21\3\21\3\22\3\22\7\22[\n\22\f\22\16\22^\13\22\2\2\23")
        buf.write("\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31")
        buf.write("\16\33\17\35\20\37\21!\22#\23\3\2\7\3\2\62;\5\2\13\f\17")
        buf.write("\17\"\"\3\2\13\u0080\5\2C\\aac|\6\2\62;C\\aac|a\2\3\3")
        buf.write("\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2")
        buf.write("\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2")
        buf.write("\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2")
        buf.write("\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\3%\3\2")
        buf.write("\2\2\5\'\3\2\2\2\7)\3\2\2\2\t+\3\2\2\2\13/\3\2\2\2\r\64")
        buf.write("\3\2\2\2\17:\3\2\2\2\21<\3\2\2\2\23>\3\2\2\2\25@\3\2\2")
        buf.write("\2\27B\3\2\2\2\31D\3\2\2\2\33G\3\2\2\2\35K\3\2\2\2\37")
        buf.write("N\3\2\2\2!T\3\2\2\2#X\3\2\2\2%&\7*\2\2&\4\3\2\2\2\'(\7")
        buf.write("+\2\2(\6\3\2\2\2)*\7=\2\2*\b\3\2\2\2+,\7k\2\2,-\7p\2\2")
        buf.write("-.\7v\2\2.\n\3\2\2\2/\60\7e\2\2\60\61\7j\2\2\61\62\7c")
        buf.write("\2\2\62\63\7t\2\2\63\f\3\2\2\2\64\65\7h\2\2\65\66\7n\2")
        buf.write("\2\66\67\7q\2\2\678\7c\2\289\7v\2\29\16\3\2\2\2:;\7?\2")
        buf.write("\2;\20\3\2\2\2<=\7/\2\2=\22\3\2\2\2>?\7-\2\2?\24\3\2\2")
        buf.write("\2@A\7,\2\2A\26\3\2\2\2BC\7\61\2\2C\30\3\2\2\2DE\7\60")
        buf.write("\2\2E\32\3\2\2\2FH\t\2\2\2GF\3\2\2\2HI\3\2\2\2IG\3\2\2")
        buf.write("\2IJ\3\2\2\2J\34\3\2\2\2KL\7)\2\2L\36\3\2\2\2MO\t\3\2")
        buf.write("\2NM\3\2\2\2OP\3\2\2\2PN\3\2\2\2PQ\3\2\2\2QR\3\2\2\2R")
        buf.write("S\b\20\2\2S \3\2\2\2TU\5\35\17\2UV\t\4\2\2VW\5\35\17\2")
        buf.write("W\"\3\2\2\2X\\\t\5\2\2Y[\t\6\2\2ZY\3\2\2\2[^\3\2\2\2\\")
        buf.write("Z\3\2\2\2\\]\3\2\2\2]$\3\2\2\2^\\\3\2\2\2\6\2IP\\\3\b")
        buf.write("\2\2")
        return buf.getvalue()


class smallCLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]


    OPEN_BRACKET = 1
    CLOSE_BRACKET = 2
    SEMICOLON = 3
    INT_TYPE = 4
    CHAR_TYPE = 5
    FLOAT_TYPE = 6
    EQUALS = 7
    MINUS = 8
    PLUS = 9
    STAR = 10
    FORWARD_SLASH = 11
    DOT = 12
    DIGIT = 13
    SINGLE_QUOTE = 14
    WHITE_SPACE = 15
    ASCII_CHARACTER = 16
    VARIABLE = 17

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'('", "')'", "';'", "'int'", "'char'", "'float'", "'='", "'-'", 
            "'+'", "'*'", "'/'", "'.'", "'''" ]

    symbolicNames = [ "<INVALID>",
            "OPEN_BRACKET", "CLOSE_BRACKET", "SEMICOLON", "INT_TYPE", "CHAR_TYPE", 
            "FLOAT_TYPE", "EQUALS", "MINUS", "PLUS", "STAR", "FORWARD_SLASH", 
            "DOT", "DIGIT", "SINGLE_QUOTE", "WHITE_SPACE", "ASCII_CHARACTER", 
            "VARIABLE" ]

    ruleNames = [ "OPEN_BRACKET", "CLOSE_BRACKET", "SEMICOLON", "INT_TYPE", 
                  "CHAR_TYPE", "FLOAT_TYPE", "EQUALS", "MINUS", "PLUS", 
                  "STAR", "FORWARD_SLASH", "DOT", "DIGIT", "SINGLE_QUOTE", 
                  "WHITE_SPACE", "ASCII_CHARACTER", "VARIABLE" ]

    grammarFileName = "smallC.g4"

    def __init__(self, input=None):
        super().__init__(input)
        self.checkVersion("4.6")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


