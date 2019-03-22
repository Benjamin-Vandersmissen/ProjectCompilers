# Generated from smallC.g4 by ANTLR 4.6
from antlr4 import *
from io import StringIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\2\20")
        buf.write("S\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\5\3")
        buf.write("\5\3\6\3\6\3\6\3\6\3\6\3\7\3\7\3\7\3\7\3\7\3\7\3\b\3\b")
        buf.write("\3\t\3\t\3\n\3\n\3\13\6\13<\n\13\r\13\16\13=\3\f\3\f\3")
        buf.write("\r\6\rC\n\r\r\r\16\rD\3\r\3\r\3\16\3\16\3\16\3\16\3\17")
        buf.write("\3\17\7\17O\n\17\f\17\16\17R\13\17\2\2\20\3\3\5\4\7\5")
        buf.write("\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35")
        buf.write("\20\3\2\7\3\2\62;\5\2\13\f\17\17\"\"\3\2\13\u0080\5\2")
        buf.write("C\\aac|\6\2\62;C\\aac|U\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3")
        buf.write("\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2")
        buf.write("\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2")
        buf.write("\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\3\37\3\2\2\2\5")
        buf.write("!\3\2\2\2\7#\3\2\2\2\t%\3\2\2\2\13)\3\2\2\2\r.\3\2\2\2")
        buf.write("\17\64\3\2\2\2\21\66\3\2\2\2\238\3\2\2\2\25;\3\2\2\2\27")
        buf.write("?\3\2\2\2\31B\3\2\2\2\33H\3\2\2\2\35L\3\2\2\2\37 \7*\2")
        buf.write("\2 \4\3\2\2\2!\"\7+\2\2\"\6\3\2\2\2#$\7=\2\2$\b\3\2\2")
        buf.write("\2%&\7k\2\2&\'\7p\2\2\'(\7v\2\2(\n\3\2\2\2)*\7e\2\2*+")
        buf.write("\7j\2\2+,\7c\2\2,-\7t\2\2-\f\3\2\2\2./\7h\2\2/\60\7n\2")
        buf.write("\2\60\61\7q\2\2\61\62\7c\2\2\62\63\7v\2\2\63\16\3\2\2")
        buf.write("\2\64\65\7?\2\2\65\20\3\2\2\2\66\67\7/\2\2\67\22\3\2\2")
        buf.write("\289\7\60\2\29\24\3\2\2\2:<\t\2\2\2;:\3\2\2\2<=\3\2\2")
        buf.write("\2=;\3\2\2\2=>\3\2\2\2>\26\3\2\2\2?@\7)\2\2@\30\3\2\2")
        buf.write("\2AC\t\3\2\2BA\3\2\2\2CD\3\2\2\2DB\3\2\2\2DE\3\2\2\2E")
        buf.write("F\3\2\2\2FG\b\r\2\2G\32\3\2\2\2HI\5\27\f\2IJ\t\4\2\2J")
        buf.write("K\5\27\f\2K\34\3\2\2\2LP\t\5\2\2MO\t\6\2\2NM\3\2\2\2O")
        buf.write("R\3\2\2\2PN\3\2\2\2PQ\3\2\2\2Q\36\3\2\2\2RP\3\2\2\2\6")
        buf.write("\2=DP\3\b\2\2")
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
    DOT = 9
    DIGIT = 10
    SINGLE_QUOTE = 11
    WHITE_SPACE = 12
    ASCII_CHARACTER = 13
    VARIABLE = 14

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'('", "')'", "';'", "'int'", "'char'", "'float'", "'='", "'-'", 
            "'.'", "'''" ]

    symbolicNames = [ "<INVALID>",
            "OPEN_BRACKET", "CLOSE_BRACKET", "SEMICOLON", "INT_TYPE", "CHAR_TYPE", 
            "FLOAT_TYPE", "EQUALS", "MINUS", "DOT", "DIGIT", "SINGLE_QUOTE", 
            "WHITE_SPACE", "ASCII_CHARACTER", "VARIABLE" ]

    ruleNames = [ "OPEN_BRACKET", "CLOSE_BRACKET", "SEMICOLON", "INT_TYPE", 
                  "CHAR_TYPE", "FLOAT_TYPE", "EQUALS", "MINUS", "DOT", "DIGIT", 
                  "SINGLE_QUOTE", "WHITE_SPACE", "ASCII_CHARACTER", "VARIABLE" ]

    grammarFileName = "smallC.g4"

    def __init__(self, input=None):
        super().__init__(input)
        self.checkVersion("4.6")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


