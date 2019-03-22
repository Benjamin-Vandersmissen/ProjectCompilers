from smallCListener import smallCListener
from smallCParser import smallCParser



class customListener(smallCListener):

    # Enter a parse tree produced by smallCParser#program.
    def enterProgram(self, ctx:smallCParser.ProgramContext):
        print("PROGRAM")
        print(ctx.getText(),'\n')

    # Exit a parse tree produced by smallCParser#program.
    def exitProgram(self, ctx:smallCParser.ProgramContext):
        #print(ctx.getText())
        pass


    # Enter a parse tree produced by smallCParser#statement.
    def enterStatement(self, ctx:smallCParser.StatementContext):
        print("STATEMENT")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#statement.
    def exitStatement(self, ctx:smallCParser.StatementContext):
        #print(ctx.getText())
        pass


    # Enter a parse tree produced by smallCParser#typeName.
    def enterTypeName(self, ctx:smallCParser.TypeNameContext):
        print("TYPENAME")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#typeName.
    def exitTypeName(self, ctx:smallCParser.TypeNameContext):
        #print(ctx.getText())
        pass


    # Enter a parse tree produced by smallCParser#declaration.
    def enterDeclaration(self, ctx:smallCParser.DeclarationContext):
        print("DECLARATION")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#declaration.
    def exitDeclaration(self, ctx:smallCParser.DeclarationContext):
        #print(ctx.getText())
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
        print("INTVALUE")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#intValue.
    def exitIntValue(self, ctx:smallCParser.IntValueContext):
        pass


    # Enter a parse tree produced by smallCParser#floatValue.
    def enterFloatValue(self, ctx:smallCParser.FloatValueContext):
        print("FLOATVALUE")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#floatValue.
    def exitFloatValue(self, ctx:smallCParser.FloatValueContext):
        pass


    # Enter a parse tree produced by smallCParser#charValue.
    def enterCharValue(self, ctx:smallCParser.CharValueContext):
        print("CHARVALUE")
        print(ctx.getText(), '\n')

    # Exit a parse tree produced by smallCParser#charValue.
    def exitCharValue(self, ctx:smallCParser.CharValueContext):
        pass

