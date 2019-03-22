# Generated from smallC.g4 by ANTLR 4.6
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .smallCParser import smallCParser
else:
    from smallCParser import smallCParser

# This class defines a complete generic visitor for a parse tree produced by smallCParser.

class smallCVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by smallCParser#program.
    def visitProgram(self, ctx:smallCParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#statement.
    def visitStatement(self, ctx:smallCParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#typeName.
    def visitTypeName(self, ctx:smallCParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#declaration.
    def visitDeclaration(self, ctx:smallCParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#assignment.
    def visitAssignment(self, ctx:smallCParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#intValue.
    def visitIntValue(self, ctx:smallCParser.IntValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#floatValue.
    def visitFloatValue(self, ctx:smallCParser.FloatValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#charValue.
    def visitCharValue(self, ctx:smallCParser.CharValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#operator.
    def visitOperator(self, ctx:smallCParser.OperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#operand.
    def visitOperand(self, ctx:smallCParser.OperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#operation.
    def visitOperation(self, ctx:smallCParser.OperationContext):
        return self.visitChildren(ctx)



del smallCParser