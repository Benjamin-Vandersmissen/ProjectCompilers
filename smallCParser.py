# Generated from smallC.g4 by ANTLR 4.6
# encoding: utf-8
from antlr4 import *
from io import StringIO

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\20")
        buf.write("J\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\3\2\3\2\3\2\3\2\3\2\3\2\3\2\7\2\32\n\2\f")
        buf.write("\2\16\2\35\13\2\3\3\3\3\3\3\5\3\"\n\3\3\4\3\4\3\5\3\5")
        buf.write("\3\5\3\5\3\5\3\5\5\5,\n\5\3\6\3\6\3\6\3\6\3\6\3\6\3\6")
        buf.write("\3\6\3\6\3\6\3\6\3\6\5\6:\n\6\3\7\3\7\3\7\5\7?\n\7\3\b")
        buf.write("\3\b\3\b\3\b\3\b\5\bF\n\b\3\t\3\t\3\t\2\3\2\n\2\4\6\b")
        buf.write("\n\f\16\20\2\3\3\2\6\bK\2\22\3\2\2\2\4!\3\2\2\2\6#\3\2")
        buf.write("\2\2\b+\3\2\2\2\n9\3\2\2\2\f>\3\2\2\2\16E\3\2\2\2\20G")
        buf.write("\3\2\2\2\22\33\b\2\1\2\23\24\f\4\2\2\24\32\7\5\2\2\25")
        buf.write("\26\f\3\2\2\26\27\5\4\3\2\27\30\7\5\2\2\30\32\3\2\2\2")
        buf.write("\31\23\3\2\2\2\31\25\3\2\2\2\32\35\3\2\2\2\33\31\3\2\2")
        buf.write("\2\33\34\3\2\2\2\34\3\3\2\2\2\35\33\3\2\2\2\36\"\5\b\5")
        buf.write("\2\37\"\5\n\6\2 \"\7\20\2\2!\36\3\2\2\2!\37\3\2\2\2! ")
        buf.write("\3\2\2\2\"\5\3\2\2\2#$\t\2\2\2$\7\3\2\2\2%&\5\6\4\2&\'")
        buf.write("\7\20\2\2\',\3\2\2\2()\5\6\4\2)*\5\n\6\2*,\3\2\2\2+%\3")
        buf.write("\2\2\2+(\3\2\2\2,\t\3\2\2\2-.\7\20\2\2./\7\t\2\2/:\7\20")
        buf.write("\2\2\60\61\7\20\2\2\61\62\7\t\2\2\62:\5\f\7\2\63\64\7")
        buf.write("\20\2\2\64\65\7\t\2\2\65:\5\16\b\2\66\67\7\20\2\2\678")
        buf.write("\7\t\2\28:\5\20\t\29-\3\2\2\29\60\3\2\2\29\63\3\2\2\2")
        buf.write("9\66\3\2\2\2:\13\3\2\2\2;<\7\n\2\2<?\7\f\2\2=?\7\f\2\2")
        buf.write(">;\3\2\2\2>=\3\2\2\2?\r\3\2\2\2@F\5\f\7\2AB\5\f\7\2BC")
        buf.write("\7\13\2\2CD\7\f\2\2DF\3\2\2\2E@\3\2\2\2EA\3\2\2\2F\17")
        buf.write("\3\2\2\2GH\7\17\2\2H\21\3\2\2\2\t\31\33!+9>E")
        return buf.getvalue()


class smallCParser ( Parser ):

    grammarFileName = "smallC.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "';'", "'int'", "'char'", 
                     "'float'", "'='", "'-'", "'.'", "<INVALID>", "'''" ]

    symbolicNames = [ "<INVALID>", "OPEN_BRACKET", "CLOSE_BRACKET", "SEMICOLON", 
                      "INT_TYPE", "CHAR_TYPE", "FLOAT_TYPE", "EQUALS", "MINUS", 
                      "DOT", "DIGIT", "SINGLE_QUOTE", "WHITE_SPACE", "ASCII_CHARACTER", 
                      "VARIABLE" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_typeName = 2
    RULE_declaration = 3
    RULE_assignment = 4
    RULE_intValue = 5
    RULE_floatValue = 6
    RULE_charValue = 7

    ruleNames =  [ "program", "statement", "typeName", "declaration", "assignment", 
                   "intValue", "floatValue", "charValue" ]

    EOF = Token.EOF
    OPEN_BRACKET=1
    CLOSE_BRACKET=2
    SEMICOLON=3
    INT_TYPE=4
    CHAR_TYPE=5
    FLOAT_TYPE=6
    EQUALS=7
    MINUS=8
    DOT=9
    DIGIT=10
    SINGLE_QUOTE=11
    WHITE_SPACE=12
    ASCII_CHARACTER=13
    VARIABLE=14

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
            self.state = 25
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 23
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                    if la_ == 1:
                        localctx = smallCParser.ProgramContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_program)
                        self.state = 17
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 18
                        self.match(smallCParser.SEMICOLON)
                        pass

                    elif la_ == 2:
                        localctx = smallCParser.ProgramContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_program)
                        self.state = 19
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 20
                        self.statement()
                        self.state = 21
                        self.match(smallCParser.SEMICOLON)
                        pass

             
                self.state = 27
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


        def VARIABLE(self):
            return self.getToken(smallCParser.VARIABLE, 0)

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
            self.state = 31
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 28
                self.declaration()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 29
                self.assignment()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 30
                self.match(smallCParser.VARIABLE)
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




    def typeName(self):

        localctx = smallCParser.TypeNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_typeName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 33
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << smallCParser.INT_TYPE) | (1 << smallCParser.CHAR_TYPE) | (1 << smallCParser.FLOAT_TYPE))) != 0)):
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
            self.state = 41
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 35
                self.typeName()
                self.state = 36
                self.match(smallCParser.VARIABLE)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 38
                self.typeName()
                self.state = 39
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

        def VARIABLE(self, i:int=None):
            if i is None:
                return self.getTokens(smallCParser.VARIABLE)
            else:
                return self.getToken(smallCParser.VARIABLE, i)

        def EQUALS(self):
            return self.getToken(smallCParser.EQUALS, 0)

        def intValue(self):
            return self.getTypedRuleContext(smallCParser.IntValueContext,0)


        def floatValue(self):
            return self.getTypedRuleContext(smallCParser.FloatValueContext,0)


        def charValue(self):
            return self.getTypedRuleContext(smallCParser.CharValueContext,0)


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
            self.state = 55
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 43
                self.match(smallCParser.VARIABLE)
                self.state = 44
                self.match(smallCParser.EQUALS)
                self.state = 45
                self.match(smallCParser.VARIABLE)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 46
                self.match(smallCParser.VARIABLE)
                self.state = 47
                self.match(smallCParser.EQUALS)
                self.state = 48
                self.intValue()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 49
                self.match(smallCParser.VARIABLE)
                self.state = 50
                self.match(smallCParser.EQUALS)
                self.state = 51
                self.floatValue()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 52
                self.match(smallCParser.VARIABLE)
                self.state = 53
                self.match(smallCParser.EQUALS)
                self.state = 54
                self.charValue()
                pass


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
            self.state = 60
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [smallCParser.MINUS]:
                self.enterOuterAlt(localctx, 1)
                self.state = 57
                self.match(smallCParser.MINUS)
                self.state = 58
                self.match(smallCParser.DIGIT)
                pass
            elif token in [smallCParser.DIGIT]:
                self.enterOuterAlt(localctx, 2)
                self.state = 59
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
            self.state = 67
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 62
                self.intValue()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 63
                self.intValue()
                self.state = 64
                self.match(smallCParser.DOT)
                self.state = 65
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
            self.state = 69
            self.match(smallCParser.ASCII_CHARACTER)
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
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def program_sempred(self, localctx:ProgramContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 1)
         




