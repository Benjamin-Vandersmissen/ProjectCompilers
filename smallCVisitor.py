# Generated from smallC.g4 by ANTLR 4.7.2
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


    # Visit a parse tree produced by smallCParser#globalDeclaration.
    def visitGlobalDeclaration(self, ctx:smallCParser.GlobalDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#codeBody.
    def visitCodeBody(self, ctx:smallCParser.CodeBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#statement.
    def visitStatement(self, ctx:smallCParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#returnStatement.
    def visitReturnStatement(self, ctx:smallCParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#constantProduct.
    def visitConstantProduct(self, ctx:smallCParser.ConstantProductContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#constantSum.
    def visitConstantSum(self, ctx:smallCParser.ConstantSumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#constantComparison.
    def visitConstantComparison(self, ctx:smallCParser.ConstantComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#constantValue.
    def visitConstantValue(self, ctx:smallCParser.ConstantValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#product.
    def visitProduct(self, ctx:smallCParser.ProductContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#comparison.
    def visitComparison(self, ctx:smallCParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#const.
    def visitConst(self, ctx:smallCParser.ConstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#sum.
    def visitSum(self, ctx:smallCParser.SumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#value.
    def visitValue(self, ctx:smallCParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#ifStatement.
    def visitIfStatement(self, ctx:smallCParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#elseStatement.
    def visitElseStatement(self, ctx:smallCParser.ElseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#whileStatement.
    def visitWhileStatement(self, ctx:smallCParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#typeName.
    def visitTypeName(self, ctx:smallCParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#declaration.
    def visitDeclaration(self, ctx:smallCParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#arrayDeclaration.
    def visitArrayDeclaration(self, ctx:smallCParser.ArrayDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#constantDeclaration.
    def visitConstantDeclaration(self, ctx:smallCParser.ConstantDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#constantArrayDeclaration.
    def visitConstantArrayDeclaration(self, ctx:smallCParser.ConstantArrayDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#arrayList.
    def visitArrayList(self, ctx:smallCParser.ArrayListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#constantArrayList.
    def visitConstantArrayList(self, ctx:smallCParser.ConstantArrayListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#arrayType.
    def visitArrayType(self, ctx:smallCParser.ArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#argumentDeclarationList.
    def visitArgumentDeclarationList(self, ctx:smallCParser.ArgumentDeclarationListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#functionDeclaration.
    def visitFunctionDeclaration(self, ctx:smallCParser.FunctionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:smallCParser.FunctionDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#returnType.
    def visitReturnType(self, ctx:smallCParser.ReturnTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#arrayElement.
    def visitArrayElement(self, ctx:smallCParser.ArrayElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#assignment.
    def visitAssignment(self, ctx:smallCParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#operatorAssignment.
    def visitOperatorAssignment(self, ctx:smallCParser.OperatorAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#constantAssignment.
    def visitConstantAssignment(self, ctx:smallCParser.ConstantAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#functionCall.
    def visitFunctionCall(self, ctx:smallCParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#argumentList.
    def visitArgumentList(self, ctx:smallCParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#operand.
    def visitOperand(self, ctx:smallCParser.OperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#constant.
    def visitConstant(self, ctx:smallCParser.ConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#identifier.
    def visitIdentifier(self, ctx:smallCParser.IdentifierContext):
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


    # Visit a parse tree produced by smallCParser#stringValue.
    def visitStringValue(self, ctx:smallCParser.StringValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#dereference.
    def visitDereference(self, ctx:smallCParser.DereferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by smallCParser#depointer.
    def visitDepointer(self, ctx:smallCParser.DepointerContext):
        return self.visitChildren(ctx)



del smallCParser