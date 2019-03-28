from smallCListener import smallCListener
from smallCParser import smallCParser



class customListener(smallCListener):
    # Enter a parse tree produced by smallCParser#program.
    def enterProgram(self, ctx:smallCParser.ProgramContext):
        print("PROGRAM")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#program.
    def exitProgram(self, ctx:smallCParser.ProgramContext):
        pass


    # Enter a parse tree produced by smallCParser#codeBody.
    def enterCodeBody(self, ctx:smallCParser.CodeBodyContext):
        print("CODE BODY")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#codeBody.
    def exitCodeBody(self, ctx:smallCParser.CodeBodyContext):
        pass


    # Enter a parse tree produced by smallCParser#statement.
    def enterStatement(self, ctx:smallCParser.StatementContext):
        print("STATEMENT")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#statement.
    def exitStatement(self, ctx:smallCParser.StatementContext):
        pass


    # Enter a parse tree produced by smallCParser#ifBlock.
    def enterIfBlock(self, ctx:smallCParser.IfBlockContext):
        print("IF BLOCK")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#ifBlock.
    def exitIfBlock(self, ctx:smallCParser.IfBlockContext):
        pass


    # Enter a parse tree produced by smallCParser#elseBlock.
    def enterElseBlock(self, ctx:smallCParser.ElseBlockContext):
        print("ELSE BLOCK")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#elseBlock.
    def exitElseBlock(self, ctx:smallCParser.ElseBlockContext):
        pass


    # Enter a parse tree produced by smallCParser#ifStatement.
    def enterIfStatement(self, ctx:smallCParser.IfStatementContext):
        print("IF STATEMENT")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#ifStatement.
    def exitIfStatement(self, ctx:smallCParser.IfStatementContext):
        pass


    # Enter a parse tree produced by smallCParser#typeName.
    def enterTypeName(self, ctx:smallCParser.TypeNameContext):
        print("TYPE NAME")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#typeName.
    def exitTypeName(self, ctx:smallCParser.TypeNameContext):
        pass


    # Enter a parse tree produced by smallCParser#declaration.
    def enterDeclaration(self, ctx:smallCParser.DeclarationContext):
        print("DECLARATION")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#declaration.
    def exitDeclaration(self, ctx:smallCParser.DeclarationContext):
        pass


    # Enter a parse tree produced by smallCParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx:smallCParser.FunctionDeclarationContext):
        print("FUNCTION DECLARATION")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx:smallCParser.FunctionDeclarationContext):
        pass


    # Enter a parse tree produced by smallCParser#argumentDeclarationList.
    def enterArgumentDeclarationList(self, ctx:smallCParser.ArgumentDeclarationListContext):
        print("ARGUMENT DECLARATION LIST")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#argumentDeclarationList.
    def exitArgumentDeclarationList(self, ctx:smallCParser.ArgumentDeclarationListContext):
        pass


    # Enter a parse tree produced by smallCParser#functionDefinition.
    def enterFunctionDefinition(self, ctx:smallCParser.FunctionDefinitionContext):
        print("FUNCTION DEFINITION")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#functionDefinition.
    def exitFunctionDefinition(self, ctx:smallCParser.FunctionDefinitionContext):
        pass


    # Enter a parse tree produced by smallCParser#returnType.
    def enterReturnType(self, ctx:smallCParser.ReturnTypeContext):
        print("RETURN TYPE")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#returnType.
    def exitReturnType(self, ctx:smallCParser.ReturnTypeContext):
        pass


    # Enter a parse tree produced by smallCParser#assignment.
    def enterAssignment(self, ctx:smallCParser.AssignmentContext):
        print("ASSIGNMENT")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#assignment.
    def exitAssignment(self, ctx:smallCParser.AssignmentContext):
        pass


    # Enter a parse tree produced by smallCParser#intValue.
    def enterIntValue(self, ctx:smallCParser.IntValueContext):
        print("INT VALUE")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#intValue.
    def exitIntValue(self, ctx:smallCParser.IntValueContext):
        pass


    # Enter a parse tree produced by smallCParser#floatValue.
    def enterFloatValue(self, ctx:smallCParser.FloatValueContext):
        print("FLOAT VALUE")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#floatValue.
    def exitFloatValue(self, ctx:smallCParser.FloatValueContext):
        pass


    # Enter a parse tree produced by smallCParser#charValue.
    def enterCharValue(self, ctx:smallCParser.CharValueContext):
        print("CHAR VALUE")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#charValue.
    def exitCharValue(self, ctx:smallCParser.CharValueContext):
        pass


    # Enter a parse tree produced by smallCParser#operator.
    def enterOperator(self, ctx:smallCParser.OperatorContext):
        print("OPERATOR")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#operator.
    def exitOperator(self, ctx:smallCParser.OperatorContext):
        pass


    # Enter a parse tree produced by smallCParser#operand.
    def enterOperand(self, ctx:smallCParser.OperandContext):
        print("OPERAND")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#operand.
    def exitOperand(self, ctx:smallCParser.OperandContext):
        pass


    # Enter a parse tree produced by smallCParser#operation.
    def enterOperation(self, ctx:smallCParser.OperationContext):
        print("OPERATION")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#operation.
    def exitOperation(self, ctx:smallCParser.OperationContext):
        pass
        
        # Enter a parse tree produced by smallCParser#whileStatement.
    def enterWhileStatement(self, ctx:smallCParser.WhileStatementContext):
        print("WHILE STATEMENT")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#whileStatement.
    def exitWhileStatement(self, ctx:smallCParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by smallCParser#whileBlock.
    def enterWhileBlock(self, ctx:smallCParser.WhileBlockContext):
        print("WHILE BLOCK")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#whileBlock.
    def exitWhileBlock(self, ctx:smallCParser.WhileBlockContext):
        pass


