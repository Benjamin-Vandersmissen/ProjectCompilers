from smallCListener import smallCListener
from smallCParser import smallCParser
from antlr4 import TerminalNode

def getRule():
    import sys
    function_name = sys._getframe(1).f_code.co_name
    if function_name.find('enter') == 0:
        return function_name[5:]
    elif function_name.find('exit') == 0:
        return function_name[4:]
    else:
        return function_name


counter = dict()
tokens = dict()
stack = list()
file = open("AST.dot", "w+")


def generateBranch(current):
    global counter, stack, file, depth

    pair = stack[-1]

    if current not in counter:
        counter[current] = 0

    if current != pair[0]:
        file.write('\t"' + pair[0] + '_' + str(pair[1]) + '" -> "' +
                    current + '_' + str(counter[current]) + '";\n')
        stack.append((current, counter[current]))
        counter[current] += 1
    elif current == pair[0]:
        stack.append(stack[-1])

def popStack(context):
    global stack, tokens
    stack = stack[:-1]

    for child in context.getChildren():
        if isinstance(child, TerminalNode):  # token
            token = str(child)
            if token in '{};(),=':  # Negeer deze tokens
                continue
            if token not in tokens:
                tokens[token] = 0
            else:
                tokens[token] += 1
            file.write('\t"' + pair[0] + '_' + str(pair[1]) + '"-> "TOKEN_' +
                       token + '_' + str(tokens[token]) + '" [style=dotted];\n')
            file.write('\t"TOKEN_' + token + '_' + str(tokens[token]) + '" [shape=plaintext];\n')

    if len(stack) == 0:
        file.write('\n}')

class customListener(smallCListener):

    # Enter a parse tree produced by smallCParser#start.
    def enterStart(self, ctx:smallCParser.StartContext):
        #
        # DOET NOG NIETS VOORLOPIG, WEET NIET WAAROM
        #
        #print("TESTETSETSETETSE")
        pass

    # Exit a parse tree produced by smallCParser#start.
    def exitStart(self, ctx:smallCParser.StartContext):
        pass


    # Enter a parse tree produced by smallCParser#program.
    def enterProgram(self, ctx:smallCParser.ProgramContext):
        global counter, file, stack
        parent = getRule()
        if parent not in counter:
            counter[parent] = 0
            file.write("digraph AST {\n")
            stack.append((parent, 0))
        else:
            counter[parent] += 1
            stack.append((parent, 0))


    # Exit a parse tree produced by smallCParser#program.
    def exitProgram(self, ctx:smallCParser.ProgramContext):
        global file
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)

    # Enter a parse tree produced by smallCParser#codeBody.
    def enterCodeBody(self, ctx:smallCParser.CodeBodyContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#codeBody.
    def exitCodeBody(self, ctx:smallCParser.CodeBodyContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#statement.
    def enterStatement(self, ctx:smallCParser.StatementContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#statement.
    def exitStatement(self, ctx:smallCParser.StatementContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#ifBlock.
    def enterIfBlock(self, ctx:smallCParser.IfBlockContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#ifBlock.
    def exitIfBlock(self, ctx:smallCParser.IfBlockContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#elseBlock.
    def enterElseBlock(self, ctx:smallCParser.ElseBlockContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#elseBlock.
    def exitElseBlock(self, ctx:smallCParser.ElseBlockContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#ifStatement.
    def enterIfStatement(self, ctx:smallCParser.IfStatementContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#ifStatement.
    def exitIfStatement(self, ctx:smallCParser.IfStatementContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#whileStatement.
    def enterWhileStatement(self, ctx:smallCParser.WhileStatementContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#whileStatement.
    def exitWhileStatement(self, ctx:smallCParser.WhileStatementContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#whileBlock.
    def enterWhileBlock(self, ctx:smallCParser.WhileBlockContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#whileBlock.
    def exitWhileBlock(self, ctx:smallCParser.WhileBlockContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#typeName.
    def enterTypeName(self, ctx:smallCParser.TypeNameContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#typeName.
    def exitTypeName(self, ctx:smallCParser.TypeNameContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#declaration.
    def enterDeclaration(self, ctx:smallCParser.DeclarationContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#declaration.
    def exitDeclaration(self, ctx:smallCParser.DeclarationContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#arrayList.
    def enterArrayList(self, ctx:smallCParser.ArrayListContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#arrayList.
    def exitArrayList(self, ctx:smallCParser.ArrayListContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx:smallCParser.FunctionDeclarationContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx:smallCParser.FunctionDeclarationContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#argumentDeclarationList.
    def enterArgumentDeclarationList(self, ctx:smallCParser.ArgumentDeclarationListContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#argumentDeclarationList.
    def exitArgumentDeclarationList(self, ctx:smallCParser.ArgumentDeclarationListContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#functionDefinition.
    def enterFunctionDefinition(self, ctx:smallCParser.FunctionDefinitionContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#functionDefinition.
    def exitFunctionDefinition(self, ctx:smallCParser.FunctionDefinitionContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#returnType.
    def enterReturnType(self, ctx:smallCParser.ReturnTypeContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#returnType.
    def exitReturnType(self, ctx:smallCParser.ReturnTypeContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#arrayElement.
    def enterArrayElement(self, ctx:smallCParser.ArrayElementContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#arrayElement.
    def exitArrayElement(self, ctx:smallCParser.ArrayElementContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#assignment.
    def enterAssignment(self, ctx:smallCParser.AssignmentContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#assignment.
    def exitAssignment(self, ctx:smallCParser.AssignmentContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#intValue.
    def enterIntValue(self, ctx:smallCParser.IntValueContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#intValue.
    def exitIntValue(self, ctx:smallCParser.IntValueContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#floatValue.
    def enterFloatValue(self, ctx:smallCParser.FloatValueContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#floatValue.
    def exitFloatValue(self, ctx:smallCParser.FloatValueContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#charValue.
    def enterCharValue(self, ctx:smallCParser.CharValueContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#charValue.
    def exitCharValue(self, ctx:smallCParser.CharValueContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#functionCall.
    def enterFunctionCall(self, ctx:smallCParser.FunctionCallContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#functionCall.
    def exitFunctionCall(self, ctx:smallCParser.FunctionCallContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#argumentList.
    def enterArgumentList(self, ctx:smallCParser.ArgumentListContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#argumentList.
    def exitArgumentList(self, ctx:smallCParser.ArgumentListContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#comparator.
    def enterComparator(self, ctx:smallCParser.ComparatorContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#comparator.
    def exitComparator(self, ctx:smallCParser.ComparatorContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#operand.
    def enterOperand(self, ctx:smallCParser.OperandContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#operand.
    def exitOperand(self, ctx:smallCParser.OperandContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#sumOperation.
    def enterSumOperation(self, ctx:smallCParser.SumOperationContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#sumOperation.
    def exitSumOperation(self, ctx:smallCParser.SumOperationContext):
        ##print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#productOperation.
    def enterProductOperation(self, ctx:smallCParser.ProductOperationContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#productOperation.
    def exitProductOperation(self, ctx:smallCParser.ProductOperationContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#operation.
    def enterOperation(self, ctx:smallCParser.OperationContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#operation.
    def exitOperation(self, ctx:smallCParser.OperationContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)

    # Enter a parse tree produced by smallCParser#identifier.
    def enterIdentifier(self, ctx:smallCParser.IdentifierContext):
        #print("Enter: ", getRule(), ctx.getText())
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#identifier.
    def exitIdentifier(self, ctx:smallCParser.IdentifierContext):
        #print("Leave: ", getRule(), ctx.getText())
        popStack(ctx)
