# Generated from smallC.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .smallCParser import smallCParser
else:
    from smallCParser import smallCParser

# This class defines a complete listener for a parse tree produced by smallCParser.
class smallCListener(ParseTreeListener):

    # Enter a parse tree produced by smallCParser#program.
    def enterProgram(self, ctx:smallCParser.ProgramContext):
        pass

    # Exit a parse tree produced by smallCParser#program.
    def exitProgram(self, ctx:smallCParser.ProgramContext):
        pass


    # Enter a parse tree produced by smallCParser#globalDeclaration.
    def enterGlobalDeclaration(self, ctx:smallCParser.GlobalDeclarationContext):
        pass

    # Exit a parse tree produced by smallCParser#globalDeclaration.
    def exitGlobalDeclaration(self, ctx:smallCParser.GlobalDeclarationContext):
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


    # Enter a parse tree produced by smallCParser#returnStatement.
    def enterReturnStatement(self, ctx:smallCParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by smallCParser#returnStatement.
    def exitReturnStatement(self, ctx:smallCParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by smallCParser#constantProduct.
    def enterConstantProduct(self, ctx:smallCParser.ConstantProductContext):
        pass

    # Exit a parse tree produced by smallCParser#constantProduct.
    def exitConstantProduct(self, ctx:smallCParser.ConstantProductContext):
        pass


    # Enter a parse tree produced by smallCParser#constantSum.
    def enterConstantSum(self, ctx:smallCParser.ConstantSumContext):
        pass

    # Exit a parse tree produced by smallCParser#constantSum.
    def exitConstantSum(self, ctx:smallCParser.ConstantSumContext):
        pass


    # Enter a parse tree produced by smallCParser#constantComparison.
    def enterConstantComparison(self, ctx:smallCParser.ConstantComparisonContext):
        pass

    # Exit a parse tree produced by smallCParser#constantComparison.
    def exitConstantComparison(self, ctx:smallCParser.ConstantComparisonContext):
        pass


    # Enter a parse tree produced by smallCParser#constantValue.
    def enterConstantValue(self, ctx:smallCParser.ConstantValueContext):
        pass

    # Exit a parse tree produced by smallCParser#constantValue.
    def exitConstantValue(self, ctx:smallCParser.ConstantValueContext):
        pass


    # Enter a parse tree produced by smallCParser#product.
    def enterProduct(self, ctx:smallCParser.ProductContext):
        pass

    # Exit a parse tree produced by smallCParser#product.
    def exitProduct(self, ctx:smallCParser.ProductContext):
        pass


    # Enter a parse tree produced by smallCParser#comparison.
    def enterComparison(self, ctx:smallCParser.ComparisonContext):
        pass

    # Exit a parse tree produced by smallCParser#comparison.
    def exitComparison(self, ctx:smallCParser.ComparisonContext):
        pass


    # Enter a parse tree produced by smallCParser#const.
    def enterConst(self, ctx:smallCParser.ConstContext):
        pass

    # Exit a parse tree produced by smallCParser#const.
    def exitConst(self, ctx:smallCParser.ConstContext):
        pass


    # Enter a parse tree produced by smallCParser#sum.
    def enterSum(self, ctx:smallCParser.SumContext):
        pass

    # Exit a parse tree produced by smallCParser#sum.
    def exitSum(self, ctx:smallCParser.SumContext):
        pass


    # Enter a parse tree produced by smallCParser#value.
    def enterValue(self, ctx:smallCParser.ValueContext):
        pass

    # Exit a parse tree produced by smallCParser#value.
    def exitValue(self, ctx:smallCParser.ValueContext):
        pass


    # Enter a parse tree produced by smallCParser#ifStatement.
    def enterIfStatement(self, ctx:smallCParser.IfStatementContext):
        pass

    # Exit a parse tree produced by smallCParser#ifStatement.
    def exitIfStatement(self, ctx:smallCParser.IfStatementContext):
        pass


    # Enter a parse tree produced by smallCParser#elseStatement.
    def enterElseStatement(self, ctx:smallCParser.ElseStatementContext):
        pass

    # Exit a parse tree produced by smallCParser#elseStatement.
    def exitElseStatement(self, ctx:smallCParser.ElseStatementContext):
        pass


    # Enter a parse tree produced by smallCParser#whileStatement.
    def enterWhileStatement(self, ctx:smallCParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by smallCParser#whileStatement.
    def exitWhileStatement(self, ctx:smallCParser.WhileStatementContext):
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


    # Enter a parse tree produced by smallCParser#arrayDeclaration.
    def enterArrayDeclaration(self, ctx:smallCParser.ArrayDeclarationContext):
        pass

    # Exit a parse tree produced by smallCParser#arrayDeclaration.
    def exitArrayDeclaration(self, ctx:smallCParser.ArrayDeclarationContext):
        pass


    # Enter a parse tree produced by smallCParser#constantDeclaration.
    def enterConstantDeclaration(self, ctx:smallCParser.ConstantDeclarationContext):
        pass

    # Exit a parse tree produced by smallCParser#constantDeclaration.
    def exitConstantDeclaration(self, ctx:smallCParser.ConstantDeclarationContext):
        pass


    # Enter a parse tree produced by smallCParser#constantArrayDeclaration.
    def enterConstantArrayDeclaration(self, ctx:smallCParser.ConstantArrayDeclarationContext):
        pass

    # Exit a parse tree produced by smallCParser#constantArrayDeclaration.
    def exitConstantArrayDeclaration(self, ctx:smallCParser.ConstantArrayDeclarationContext):
        pass


    # Enter a parse tree produced by smallCParser#arrayList.
    def enterArrayList(self, ctx:smallCParser.ArrayListContext):
        pass

    # Exit a parse tree produced by smallCParser#arrayList.
    def exitArrayList(self, ctx:smallCParser.ArrayListContext):
        pass


    # Enter a parse tree produced by smallCParser#constantArrayList.
    def enterConstantArrayList(self, ctx:smallCParser.ConstantArrayListContext):
        pass

    # Exit a parse tree produced by smallCParser#constantArrayList.
    def exitConstantArrayList(self, ctx:smallCParser.ConstantArrayListContext):
        pass


    # Enter a parse tree produced by smallCParser#arrayType.
    def enterArrayType(self, ctx:smallCParser.ArrayTypeContext):
        pass

    # Exit a parse tree produced by smallCParser#arrayType.
    def exitArrayType(self, ctx:smallCParser.ArrayTypeContext):
        pass


    # Enter a parse tree produced by smallCParser#argumentDeclarationList.
    def enterArgumentDeclarationList(self, ctx:smallCParser.ArgumentDeclarationListContext):
        pass

    # Exit a parse tree produced by smallCParser#argumentDeclarationList.
    def exitArgumentDeclarationList(self, ctx:smallCParser.ArgumentDeclarationListContext):
        pass


    # Enter a parse tree produced by smallCParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx:smallCParser.FunctionDeclarationContext):
        pass

    # Exit a parse tree produced by smallCParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx:smallCParser.FunctionDeclarationContext):
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


    # Enter a parse tree produced by smallCParser#constantAssignment.
    def enterConstantAssignment(self, ctx:smallCParser.ConstantAssignmentContext):
        pass

    # Exit a parse tree produced by smallCParser#constantAssignment.
    def exitConstantAssignment(self, ctx:smallCParser.ConstantAssignmentContext):
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


    # Enter a parse tree produced by smallCParser#operand.
    def enterOperand(self, ctx:smallCParser.OperandContext):
        pass

    # Exit a parse tree produced by smallCParser#operand.
    def exitOperand(self, ctx:smallCParser.OperandContext):
        pass


    # Enter a parse tree produced by smallCParser#constant.
    def enterConstant(self, ctx:smallCParser.ConstantContext):
        pass

    # Exit a parse tree produced by smallCParser#constant.
    def exitConstant(self, ctx:smallCParser.ConstantContext):
        pass


    # Enter a parse tree produced by smallCParser#identifier.
    def enterIdentifier(self, ctx:smallCParser.IdentifierContext):
        pass

    # Exit a parse tree produced by smallCParser#identifier.
    def exitIdentifier(self, ctx:smallCParser.IdentifierContext):
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


    # Enter a parse tree produced by smallCParser#dereference.
    def enterDereference(self, ctx:smallCParser.DereferenceContext):
        pass

    # Exit a parse tree produced by smallCParser#dereference.
    def exitDereference(self, ctx:smallCParser.DereferenceContext):
        pass


    # Enter a parse tree produced by smallCParser#depointer.
    def enterDepointer(self, ctx:smallCParser.DepointerContext):
        pass

    # Exit a parse tree produced by smallCParser#depointer.
    def exitDepointer(self, ctx:smallCParser.DepointerContext):
        pass


