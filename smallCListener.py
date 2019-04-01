# Generated from smallC.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .smallCParser import smallCParser
else:
    from smallCParser import smallCParser

# This class defines a complete listener for a parse tree produced by smallCParser.
class smallCListener(ParseTreeListener):

    # Enter a parse tree produced by smallCParser#start.
    def enterStart(self, ctx:smallCParser.StartContext):
        pass

    # Exit a parse tree produced by smallCParser#start.
    def exitStart(self, ctx:smallCParser.StartContext):
        pass


    # Enter a parse tree produced by smallCParser#program.
    def enterProgram(self, ctx:smallCParser.ProgramContext):
        pass

    # Exit a parse tree produced by smallCParser#program.
    def exitProgram(self, ctx:smallCParser.ProgramContext):
        pass


    # Enter a parse tree produced by smallCParser#codeBody.
    def enterCodeBody(self, ctx:smallCParser.CodeBodyContext):
        pass

    # Exit a parse tree produced by smallCParser#codeBody.
    def exitCodeBody(self, ctx:smallCParser.CodeBodyContext):
        pass


    # Enter a parse tree produced by smallCParser#statement.
    def enterStatement(self, ctx:smallCParser.StatementContext):
        pass

    # Exit a parse tree produced by smallCParser#statement.
    def exitStatement(self, ctx:smallCParser.StatementContext):
        pass


    # Enter a parse tree produced by smallCParser#ifBlock.
    def enterIfBlock(self, ctx:smallCParser.IfBlockContext):
        pass

    # Exit a parse tree produced by smallCParser#ifBlock.
    def exitIfBlock(self, ctx:smallCParser.IfBlockContext):
        pass


    # Enter a parse tree produced by smallCParser#elseBlock.
    def enterElseBlock(self, ctx:smallCParser.ElseBlockContext):
        pass

    # Exit a parse tree produced by smallCParser#elseBlock.
    def exitElseBlock(self, ctx:smallCParser.ElseBlockContext):
        pass


    # Enter a parse tree produced by smallCParser#ifStatement.
    def enterIfStatement(self, ctx:smallCParser.IfStatementContext):
        pass

    # Exit a parse tree produced by smallCParser#ifStatement.
    def exitIfStatement(self, ctx:smallCParser.IfStatementContext):
        pass


    # Enter a parse tree produced by smallCParser#whileStatement.
    def enterWhileStatement(self, ctx:smallCParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by smallCParser#whileStatement.
    def exitWhileStatement(self, ctx:smallCParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by smallCParser#whileBlock.
    def enterWhileBlock(self, ctx:smallCParser.WhileBlockContext):
        pass

    # Exit a parse tree produced by smallCParser#whileBlock.
    def exitWhileBlock(self, ctx:smallCParser.WhileBlockContext):
        pass


    # Enter a parse tree produced by smallCParser#typeName.
    def enterTypeName(self, ctx:smallCParser.TypeNameContext):
        pass

    # Exit a parse tree produced by smallCParser#typeName.
    def exitTypeName(self, ctx:smallCParser.TypeNameContext):
        pass


    # Enter a parse tree produced by smallCParser#declaration.
    def enterDeclaration(self, ctx:smallCParser.DeclarationContext):
        pass

    # Exit a parse tree produced by smallCParser#declaration.
    def exitDeclaration(self, ctx:smallCParser.DeclarationContext):
        pass


    # Enter a parse tree produced by smallCParser#constantDeclaration.
    def enterConstantDeclaration(self, ctx:smallCParser.ConstantDeclarationContext):
        pass

    # Exit a parse tree produced by smallCParser#constantDeclaration.
    def exitConstantDeclaration(self, ctx:smallCParser.ConstantDeclarationContext):
        pass


    # Enter a parse tree produced by smallCParser#constantArrayList.
    def enterConstantArrayList(self, ctx:smallCParser.ConstantArrayListContext):
        pass

    # Exit a parse tree produced by smallCParser#constantArrayList.
    def exitConstantArrayList(self, ctx:smallCParser.ConstantArrayListContext):
        pass


    # Enter a parse tree produced by smallCParser#constantAssignment.
    def enterConstantAssignment(self, ctx:smallCParser.ConstantAssignmentContext):
        pass

    # Exit a parse tree produced by smallCParser#constantAssignment.
    def exitConstantAssignment(self, ctx:smallCParser.ConstantAssignmentContext):
        pass


    # Enter a parse tree produced by smallCParser#constantExpression.
    def enterConstantExpression(self, ctx:smallCParser.ConstantExpressionContext):
        pass

    # Exit a parse tree produced by smallCParser#constantExpression.
    def exitConstantExpression(self, ctx:smallCParser.ConstantExpressionContext):
        pass


    # Enter a parse tree produced by smallCParser#constantSum.
    def enterConstantSum(self, ctx:smallCParser.ConstantSumContext):
        pass

    # Exit a parse tree produced by smallCParser#constantSum.
    def exitConstantSum(self, ctx:smallCParser.ConstantSumContext):
        pass


    # Enter a parse tree produced by smallCParser#constantProduct.
    def enterConstantProduct(self, ctx:smallCParser.ConstantProductContext):
        pass

    # Exit a parse tree produced by smallCParser#constantProduct.
    def exitConstantProduct(self, ctx:smallCParser.ConstantProductContext):
        pass


    # Enter a parse tree produced by smallCParser#constant.
    def enterConstant(self, ctx:smallCParser.ConstantContext):
        pass

    # Exit a parse tree produced by smallCParser#constant.
    def exitConstant(self, ctx:smallCParser.ConstantContext):
        pass


    # Enter a parse tree produced by smallCParser#arrayList.
    def enterArrayList(self, ctx:smallCParser.ArrayListContext):
        pass

    # Exit a parse tree produced by smallCParser#arrayList.
    def exitArrayList(self, ctx:smallCParser.ArrayListContext):
        pass


    # Enter a parse tree produced by smallCParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx:smallCParser.FunctionDeclarationContext):
        pass

    # Exit a parse tree produced by smallCParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx:smallCParser.FunctionDeclarationContext):
        pass


    # Enter a parse tree produced by smallCParser#argumentDeclarationList.
    def enterArgumentDeclarationList(self, ctx:smallCParser.ArgumentDeclarationListContext):
        pass

    # Exit a parse tree produced by smallCParser#argumentDeclarationList.
    def exitArgumentDeclarationList(self, ctx:smallCParser.ArgumentDeclarationListContext):
        pass


    # Enter a parse tree produced by smallCParser#functionDefinition.
    def enterFunctionDefinition(self, ctx:smallCParser.FunctionDefinitionContext):
        pass

    # Exit a parse tree produced by smallCParser#functionDefinition.
    def exitFunctionDefinition(self, ctx:smallCParser.FunctionDefinitionContext):
        pass


    # Enter a parse tree produced by smallCParser#returnType.
    def enterReturnType(self, ctx:smallCParser.ReturnTypeContext):
        pass

    # Exit a parse tree produced by smallCParser#returnType.
    def exitReturnType(self, ctx:smallCParser.ReturnTypeContext):
        pass


    # Enter a parse tree produced by smallCParser#arrayElement.
    def enterArrayElement(self, ctx:smallCParser.ArrayElementContext):
        pass

    # Exit a parse tree produced by smallCParser#arrayElement.
    def exitArrayElement(self, ctx:smallCParser.ArrayElementContext):
        pass


    # Enter a parse tree produced by smallCParser#assignment.
    def enterAssignment(self, ctx:smallCParser.AssignmentContext):
        pass

    # Exit a parse tree produced by smallCParser#assignment.
    def exitAssignment(self, ctx:smallCParser.AssignmentContext):
        pass


    # Enter a parse tree produced by smallCParser#intValue.
    def enterIntValue(self, ctx:smallCParser.IntValueContext):
        pass

    # Exit a parse tree produced by smallCParser#intValue.
    def exitIntValue(self, ctx:smallCParser.IntValueContext):
        pass


    # Enter a parse tree produced by smallCParser#floatValue.
    def enterFloatValue(self, ctx:smallCParser.FloatValueContext):
        pass

    # Exit a parse tree produced by smallCParser#floatValue.
    def exitFloatValue(self, ctx:smallCParser.FloatValueContext):
        pass


    # Enter a parse tree produced by smallCParser#charValue.
    def enterCharValue(self, ctx:smallCParser.CharValueContext):
        pass

    # Exit a parse tree produced by smallCParser#charValue.
    def exitCharValue(self, ctx:smallCParser.CharValueContext):
        pass


    # Enter a parse tree produced by smallCParser#functionCall.
    def enterFunctionCall(self, ctx:smallCParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by smallCParser#functionCall.
    def exitFunctionCall(self, ctx:smallCParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by smallCParser#argumentList.
    def enterArgumentList(self, ctx:smallCParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by smallCParser#argumentList.
    def exitArgumentList(self, ctx:smallCParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by smallCParser#comparator.
    def enterComparator(self, ctx:smallCParser.ComparatorContext):
        pass

    # Exit a parse tree produced by smallCParser#comparator.
    def exitComparator(self, ctx:smallCParser.ComparatorContext):
        pass


    # Enter a parse tree produced by smallCParser#operand.
    def enterOperand(self, ctx:smallCParser.OperandContext):
        pass

    # Exit a parse tree produced by smallCParser#operand.
    def exitOperand(self, ctx:smallCParser.OperandContext):
        pass


    # Enter a parse tree produced by smallCParser#sumOperation.
    def enterSumOperation(self, ctx:smallCParser.SumOperationContext):
        pass

    # Exit a parse tree produced by smallCParser#sumOperation.
    def exitSumOperation(self, ctx:smallCParser.SumOperationContext):
        pass


    # Enter a parse tree produced by smallCParser#productOperation.
    def enterProductOperation(self, ctx:smallCParser.ProductOperationContext):
        pass

    # Exit a parse tree produced by smallCParser#productOperation.
    def exitProductOperation(self, ctx:smallCParser.ProductOperationContext):
        pass


    # Enter a parse tree produced by smallCParser#operation.
    def enterOperation(self, ctx:smallCParser.OperationContext):
        pass

    # Exit a parse tree produced by smallCParser#operation.
    def exitOperation(self, ctx:smallCParser.OperationContext):
        pass


    # Enter a parse tree produced by smallCParser#identifier.
    def enterIdentifier(self, ctx:smallCParser.IdentifierContext):
        pass

    # Exit a parse tree produced by smallCParser#identifier.
    def exitIdentifier(self, ctx:smallCParser.IdentifierContext):
        pass


