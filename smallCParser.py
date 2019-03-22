# Generated from smallC.g4 by ANTLR 4.6
# encoding: utf-8
from antlr4 import *
from io import StringIO

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\34")
        buf.write("h\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\3\2\3\2\3\2\3\2")
        buf.write("\3\2\3\2\3\2\3\2\3\2\7\2\"\n\2\f\2\16\2%\13\2\3\3\3\3")
        buf.write("\3\3\5\3*\n\3\3\4\3\4\3\4\3\4\5\4\60\n\4\3\4\3\4\7\4\64")
        buf.write("\n\4\f\4\16\4\67\13\4\3\5\3\5\3\5\3\5\3\5\3\5\5\5?\n\5")
        buf.write("\3\6\3\6\3\6\3\6\3\7\3\7\3\7\3\7\3\7\5\7J\n\7\3\b\3\b")
        buf.write("\3\b\3\b\3\b\5\bQ\n\b\3\t\3\t\3\n\3\n\3\13\3\13\3\13\3")
        buf.write("\13\5\13[\n\13\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\5\f")
        buf.write("f\n\f\3\f\2\4\2\6\r\2\4\6\b\n\f\16\20\22\24\26\2\3\3\2")
        buf.write("\n\20m\2\30\3\2\2\2\4)\3\2\2\2\6/\3\2\2\2\b>\3\2\2\2\n")
        buf.write("@\3\2\2\2\fI\3\2\2\2\16P\3\2\2\2\20R\3\2\2\2\22T\3\2\2")
        buf.write("\2\24Z\3\2\2\2\26e\3\2\2\2\30#\b\2\1\2\31\32\f\5\2\2\32")
        buf.write("\"\7\5\2\2\33\34\f\4\2\2\34\35\5\4\3\2\35\36\7\5\2\2\36")
        buf.write("\"\3\2\2\2\37 \f\3\2\2 \"\7\33\2\2!\31\3\2\2\2!\33\3\2")
        buf.write("\2\2!\37\3\2\2\2\"%\3\2\2\2#!\3\2\2\2#$\3\2\2\2$\3\3\2")
        buf.write("\2\2%#\3\2\2\2&*\5\b\5\2\'*\5\n\6\2(*\5\26\f\2)&\3\2\2")
        buf.write("\2)\'\3\2\2\2)(\3\2\2\2*\5\3\2\2\2+,\b\4\1\2,\60\7\6\2")
        buf.write("\2-\60\7\7\2\2.\60\7\b\2\2/+\3\2\2\2/-\3\2\2\2/.\3\2\2")
        buf.write("\2\60\65\3\2\2\2\61\62\f\3\2\2\62\64\7\f\2\2\63\61\3\2")
        buf.write("\2\2\64\67\3\2\2\2\65\63\3\2\2\2\65\66\3\2\2\2\66\7\3")
        buf.write("\2\2\2\67\65\3\2\2\289\5\6\4\29:\7\32\2\2:?\3\2\2\2;<")
        buf.write("\5\6\4\2<=\5\n\6\2=?\3\2\2\2>8\3\2\2\2>;\3\2\2\2?\t\3")
        buf.write("\2\2\2@A\7\32\2\2AB\7\t\2\2BC\5\26\f\2C\13\3\2\2\2DE\7")
        buf.write("\n\2\2EJ\7\22\2\2FG\7\13\2\2GJ\7\22\2\2HJ\7\22\2\2ID\3")
        buf.write("\2\2\2IF\3\2\2\2IH\3\2\2\2J\r\3\2\2\2KQ\5\f\7\2LM\5\f")
        buf.write("\7\2MN\7\21\2\2NO\7\22\2\2OQ\3\2\2\2PK\3\2\2\2PL\3\2\2")
        buf.write("\2Q\17\3\2\2\2RS\7\25\2\2S\21\3\2\2\2TU\t\2\2\2U\23\3")
        buf.write("\2\2\2V[\7\32\2\2W[\5\f\7\2X[\5\16\b\2Y[\5\20\t\2ZV\3")
        buf.write("\2\2\2ZW\3\2\2\2ZX\3\2\2\2ZY\3\2\2\2[\25\3\2\2\2\\]\5")
        buf.write("\24\13\2]^\5\22\n\2^_\5\26\f\2_f\3\2\2\2`f\5\24\13\2a")
        buf.write("b\7\3\2\2bc\5\26\f\2cd\7\4\2\2df\3\2\2\2e\\\3\2\2\2e`")
        buf.write("\3\2\2\2ea\3\2\2\2f\27\3\2\2\2\f!#)/\65>IPZe")
        return buf.getvalue()


class smallCParser ( Parser ):

    grammarFileName = "smallC.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "';'", "'int'", "'char'", 
                     "'float'", "'='", "'-'", "'+'", "'*'", "'/'", "'>'", 
                     "'<'", "'=='", "'.'", "<INVALID>", "'''", "<INVALID>", 
                     "<INVALID>", "'if'", "'else'", "'while'", "'return'" ]

    symbolicNames = [ "<INVALID>", "OPEN_BRACKET", "CLOSE_BRACKET", "SEMICOLON", 
                      "INT_TYPE", "CHAR_TYPE", "FLOAT_TYPE", "ASSIGN", "MINUS", 
                      "PLUS", "STAR", "FORWARD_SLASH", "LARGER_THAN", "SMALLER_THAN", 
                      "EQUALS", "DOT", "DIGIT", "SINGLE_QUOTE", "WHITE_SPACE", 
                      "ASCII_CHARACTER", "IF", "ELSE", "WHILE", "RETURN", 
                      "VARIABLE", "SINGLE_LINE_COMMENT", "MULTI_LINE_COMMENT" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_typeName = 2
    RULE_declaration = 3
    RULE_assignment = 4
    RULE_intValue = 5
    RULE_floatValue = 6
    RULE_charValue = 7
    RULE_operator = 8
    RULE_operand = 9
    RULE_operation = 10

    ruleNames =  [ "program", "statement", "typeName", "declaration", "assignment", 
                   "intValue", "floatValue", "charValue", "operator", "operand", 
                   "operation" ]

    EOF = Token.EOF
    OPEN_BRACKET=1
    CLOSE_BRACKET=2
    SEMICOLON=3
    INT_TYPE=4
    CHAR_TYPE=5
    FLOAT_TYPE=6
    ASSIGN=7
    MINUS=8
    PLUS=9
    STAR=10
    FORWARD_SLASH=11
    LARGER_THAN=12
    SMALLER_THAN=13
    EQUALS=14
    DOT=15
    DIGIT=16
    SINGLE_QUOTE=17
    WHITE_SPACE=18
    ASCII_CHARACTER=19
    IF=20
    ELSE=21
    WHILE=22
    RETURN=23
    VARIABLE=24
    SINGLE_LINE_COMMENT=25
    MULTI_LINE_COMMENT=26

    def __init__(self, input:TokenStream):
        super().__init__(input)
        self.checkVersion("4.6")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class ProgramContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def program(self):
            return self.getTypedRuleContext(smallCParser.ProgramContext,0)


        def SEMICOLON(self):
            return self.getToken(smallCParser.SEMICOLON, 0)

        def statement(self):
            return self.getTypedRuleContext(smallCParser.StatementContext,0)


        def SINGLE_LINE_COMMENT(self):
            return self.getToken(smallCParser.SINGLE_LINE_COMMENT, 0)

        def getRuleIndex(self):
            return smallCParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)



    def program(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = smallCParser.ProgramContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 0
        self.enterRecursionRule(localctx, 0, self.RULE_program, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self._ctx.stop = self._input.LT(-1)
            self.state = 33
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 31
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                    if la_ == 1:
                        localctx = smallCParser.ProgramContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_program)
                        self.state = 23
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 24
                        self.match(smallCParser.SEMICOLON)
                        pass

                    elif la_ == 2:
                        localctx = smallCParser.ProgramContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_program)
                        self.state = 25
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 26
                        self.statement()
                        self.state = 27
                        self.match(smallCParser.SEMICOLON)
                        pass

                    elif la_ == 3:
                        localctx = smallCParser.ProgramContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_program)
                        self.state = 29
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 30
                        self.match(smallCParser.SINGLE_LINE_COMMENT)
                        pass

             
                self.state = 35
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class StatementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def declaration(self):
            return self.getTypedRuleContext(smallCParser.DeclarationContext,0)


        def assignment(self):
            return self.getTypedRuleContext(smallCParser.AssignmentContext,0)


        def operation(self):
            return self.getTypedRuleContext(smallCParser.OperationContext,0)


        def getRuleIndex(self):
            return smallCParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = smallCParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 39
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 36
                self.declaration()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 37
                self.assignment()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 38
                self.operation()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TypeNameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT_TYPE(self):
            return self.getToken(smallCParser.INT_TYPE, 0)

        def CHAR_TYPE(self):
            return self.getToken(smallCParser.CHAR_TYPE, 0)

        def FLOAT_TYPE(self):
            return self.getToken(smallCParser.FLOAT_TYPE, 0)

        def typeName(self):
            return self.getTypedRuleContext(smallCParser.TypeNameContext,0)


        def STAR(self):
            return self.getToken(smallCParser.STAR, 0)

        def getRuleIndex(self):
            return smallCParser.RULE_typeName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeName" ):
                listener.enterTypeName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeName" ):
                listener.exitTypeName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeName" ):
                return visitor.visitTypeName(self)
            else:
                return visitor.visitChildren(self)



    def typeName(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = smallCParser.TypeNameContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 4
        self.enterRecursionRule(localctx, 4, self.RULE_typeName, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [smallCParser.INT_TYPE]:
                self.state = 42
                self.match(smallCParser.INT_TYPE)
                pass
            elif token in [smallCParser.CHAR_TYPE]:
                self.state = 43
                self.match(smallCParser.CHAR_TYPE)
                pass
            elif token in [smallCParser.FLOAT_TYPE]:
                self.state = 44
                self.match(smallCParser.FLOAT_TYPE)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 51
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = smallCParser.TypeNameContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_typeName)
                    self.state = 47
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 48
                    self.match(smallCParser.STAR) 
                self.state = 53
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class DeclarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeName(self):
            return self.getTypedRuleContext(smallCParser.TypeNameContext,0)


        def VARIABLE(self):
            return self.getToken(smallCParser.VARIABLE, 0)

        def assignment(self):
            return self.getTypedRuleContext(smallCParser.AssignmentContext,0)


        def getRuleIndex(self):
            return smallCParser.RULE_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaration" ):
                listener.enterDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaration" ):
                listener.exitDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclaration" ):
                return visitor.visitDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def declaration(self):

        localctx = smallCParser.DeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_declaration)
        try:
            self.state = 60
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 54
                self.typeName(0)
                self.state = 55
                self.match(smallCParser.VARIABLE)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 57
                self.typeName(0)
                self.state = 58
                self.assignment()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AssignmentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VARIABLE(self):
            return self.getToken(smallCParser.VARIABLE, 0)

        def ASSIGN(self):
            return self.getToken(smallCParser.ASSIGN, 0)

        def operation(self):
            return self.getTypedRuleContext(smallCParser.OperationContext,0)


        def getRuleIndex(self):
            return smallCParser.RULE_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = smallCParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self.match(smallCParser.VARIABLE)
            self.state = 63
            self.match(smallCParser.ASSIGN)
            self.state = 64
            self.operation()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class IntValueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MINUS(self):
            return self.getToken(smallCParser.MINUS, 0)

        def DIGIT(self):
            return self.getToken(smallCParser.DIGIT, 0)

        def PLUS(self):
            return self.getToken(smallCParser.PLUS, 0)

        def getRuleIndex(self):
            return smallCParser.RULE_intValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntValue" ):
                listener.enterIntValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntValue" ):
                listener.exitIntValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIntValue" ):
                return visitor.visitIntValue(self)
            else:
                return visitor.visitChildren(self)




    def intValue(self):

        localctx = smallCParser.IntValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_intValue)
        try:
            self.state = 71
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [smallCParser.MINUS]:
                self.enterOuterAlt(localctx, 1)
                self.state = 66
                self.match(smallCParser.MINUS)
                self.state = 67
                self.match(smallCParser.DIGIT)
                pass
            elif token in [smallCParser.PLUS]:
                self.enterOuterAlt(localctx, 2)
                self.state = 68
                self.match(smallCParser.PLUS)
                self.state = 69
                self.match(smallCParser.DIGIT)
                pass
            elif token in [smallCParser.DIGIT]:
                self.enterOuterAlt(localctx, 3)
                self.state = 70
                self.match(smallCParser.DIGIT)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FloatValueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def intValue(self):
            return self.getTypedRuleContext(smallCParser.IntValueContext,0)


        def DOT(self):
            return self.getToken(smallCParser.DOT, 0)

        def DIGIT(self):
            return self.getToken(smallCParser.DIGIT, 0)

        def getRuleIndex(self):
            return smallCParser.RULE_floatValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFloatValue" ):
                listener.enterFloatValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFloatValue" ):
                listener.exitFloatValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFloatValue" ):
                return visitor.visitFloatValue(self)
            else:
                return visitor.visitChildren(self)




    def floatValue(self):

        localctx = smallCParser.FloatValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_floatValue)
        try:
            self.state = 78
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 73
                self.intValue()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 74
                self.intValue()
                self.state = 75
                self.match(smallCParser.DOT)
                self.state = 76
                self.match(smallCParser.DIGIT)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CharValueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ASCII_CHARACTER(self):
            return self.getToken(smallCParser.ASCII_CHARACTER, 0)

        def getRuleIndex(self):
            return smallCParser.RULE_charValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharValue" ):
                listener.enterCharValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharValue" ):
                listener.exitCharValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCharValue" ):
                return visitor.visitCharValue(self)
            else:
                return visitor.visitChildren(self)




    def charValue(self):

        localctx = smallCParser.CharValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_charValue)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            self.match(smallCParser.ASCII_CHARACTER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class OperatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLUS(self):
            return self.getToken(smallCParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(smallCParser.MINUS, 0)

        def STAR(self):
            return self.getToken(smallCParser.STAR, 0)

        def FORWARD_SLASH(self):
            return self.getToken(smallCParser.FORWARD_SLASH, 0)

        def LARGER_THAN(self):
            return self.getToken(smallCParser.LARGER_THAN, 0)

        def SMALLER_THAN(self):
            return self.getToken(smallCParser.SMALLER_THAN, 0)

        def EQUALS(self):
            return self.getToken(smallCParser.EQUALS, 0)

        def getRuleIndex(self):
            return smallCParser.RULE_operator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOperator" ):
                listener.enterOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOperator" ):
                listener.exitOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOperator" ):
                return visitor.visitOperator(self)
            else:
                return visitor.visitChildren(self)




    def operator(self):

        localctx = smallCParser.OperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_operator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << smallCParser.MINUS) | (1 << smallCParser.PLUS) | (1 << smallCParser.STAR) | (1 << smallCParser.FORWARD_SLASH) | (1 << smallCParser.LARGER_THAN) | (1 << smallCParser.SMALLER_THAN) | (1 << smallCParser.EQUALS))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class OperandContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VARIABLE(self):
            return self.getToken(smallCParser.VARIABLE, 0)

        def intValue(self):
            return self.getTypedRuleContext(smallCParser.IntValueContext,0)


        def floatValue(self):
            return self.getTypedRuleContext(smallCParser.FloatValueContext,0)


        def charValue(self):
            return self.getTypedRuleContext(smallCParser.CharValueContext,0)


        def getRuleIndex(self):
            return smallCParser.RULE_operand

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOperand" ):
                listener.enterOperand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOperand" ):
                listener.exitOperand(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOperand" ):
                return visitor.visitOperand(self)
            else:
                return visitor.visitChildren(self)




    def operand(self):

        localctx = smallCParser.OperandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_operand)
        try:
            self.state = 88
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 84
                self.match(smallCParser.VARIABLE)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 85
                self.intValue()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 86
                self.floatValue()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 87
                self.charValue()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class OperationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def operand(self):
            return self.getTypedRuleContext(smallCParser.OperandContext,0)


        def operator(self):
            return self.getTypedRuleContext(smallCParser.OperatorContext,0)


        def operation(self):
            return self.getTypedRuleContext(smallCParser.OperationContext,0)


        def OPEN_BRACKET(self):
            return self.getToken(smallCParser.OPEN_BRACKET, 0)

        def CLOSE_BRACKET(self):
            return self.getToken(smallCParser.CLOSE_BRACKET, 0)

        def getRuleIndex(self):
            return smallCParser.RULE_operation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOperation" ):
                listener.enterOperation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOperation" ):
                listener.exitOperation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOperation" ):
                return visitor.visitOperation(self)
            else:
                return visitor.visitChildren(self)




    def operation(self):

        localctx = smallCParser.OperationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_operation)
        try:
            self.state = 99
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 90
                self.operand()
                self.state = 91
                self.operator()
                self.state = 92
                self.operation()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 94
                self.operand()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 95
                self.match(smallCParser.OPEN_BRACKET)
                self.state = 96
                self.operation()
                self.state = 97
                self.match(smallCParser.CLOSE_BRACKET)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[0] = self.program_sempred
        self._predicates[2] = self.typeName_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def program_sempred(self, localctx:ProgramContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 1)
         

    def typeName_sempred(self, localctx:TypeNameContext, predIndex:int):
            if predIndex == 3:
                return self.precpred(self._ctx, 1)
         




