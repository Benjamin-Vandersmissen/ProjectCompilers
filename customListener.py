from smallCListener import smallCListener
from smallCParser import smallCParser
from antlr4 import TerminalNode
#
# TODO: BUGS OPLOSSEN :
#               START WILT NIET WERKEN ALS OFFICIELE START VAN GRAMMATICA, DUS KOMT ER MEERMAALS digraph VOOR IN DE AST
#
#

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
file = open("AST.dot", "a")

def generateBranch(current):
    global counter, stack, file
    if current not in counter:
        counter[current] = 0
    else:
        counter[current] += 1

    pair = stack[-1]
    if current != pair[0]:
        file.write('\t"' + pair[0] + '_' + str(pair[1]) + '" -> "' +
                    current + '_' + str(counter[current]) + '";\n')
        stack.append((current, counter[current]))

def popStack(context):
    global stack, tokens
    pair = stack[-1]
    if pair[1] < counter[pair[0]]:
        #
        # EXAMPLE : if we have 4 codebodies we merge, then we need to append everything from codebody 0 - 3 on
        #           codebody 0.
        #           If we finish codebody 3, we go up a level and decrease the counter of codebody.
        #           If the counter is equal to value on the stack (0 in this case),
        #           we know we have left the original codebody.
        #
        counter[pair[0]] = counter[pair[0]]-1
    elif pair[1] == counter[pair[0]]:
        stack = stack[:-1]

    for child in context.getChildren():
        if isinstance(child, TerminalNode):  # token
            token = str(child)
            if token in '{};':  # Negeer deze tokens
                continue
            if token not in tokens:
                tokens[token] = 0
            else:
                tokens[token] += 1
            file.write('\t"' + pair[0] + '_' + str(pair[1]) + '"-> "TOKEN_' +
                       token + '_' + str(tokens[token]) + '" [style=dotted];\n')
            file.write('\t"TOKEN_' + token + '_' + str(tokens[token]) + '" [shape=plaintext];\n')



class customListener(smallCListener):

    # Enter a parse tree produced by smallCParser#start.
    def enterStart(self, ctx:smallCParser.StartContext):
        #
        # DOET NOG NIETS VOORLOPIG, WEET NIET WAAROM
        #
        print("TESTETSETSETETSE")
        pass

    # Exit a parse tree produced by smallCParser#start.
    def exitStart(self, ctx:smallCParser.StartContext):
        pass


    # Enter a parse tree produced by smallCParser#program.
    def enterProgram(self, ctx:smallCParser.ProgramContext):
        global counter,file
        parent = "start"
        counter[parent] = 0
        stack.append((parent, 0))
        generateBranch(getRule())



    # Exit a parse tree produced by smallCParser#program.
    def exitProgram(self, ctx:smallCParser.ProgramContext):
        popStack(ctx)

    # Enter a parse tree produced by smallCParser#codeBody.
    def enterCodeBody(self, ctx:smallCParser.CodeBodyContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#codeBody.
    def exitCodeBody(self, ctx:smallCParser.CodeBodyContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#statement.
    def enterStatement(self, ctx:smallCParser.StatementContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#statement.
    def exitStatement(self, ctx:smallCParser.StatementContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#ifBlock.
    def enterIfBlock(self, ctx:smallCParser.IfBlockContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#ifBlock.
    def exitIfBlock(self, ctx:smallCParser.IfBlockContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#elseBlock.
    def enterElseBlock(self, ctx:smallCParser.ElseBlockContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#elseBlock.
    def exitElseBlock(self, ctx:smallCParser.ElseBlockContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#ifStatement.
    def enterIfStatement(self, ctx:smallCParser.IfStatementContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#ifStatement.
    def exitIfStatement(self, ctx:smallCParser.IfStatementContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#whileStatement.
    def enterWhileStatement(self, ctx:smallCParser.WhileStatementContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#whileStatement.
    def exitWhileStatement(self, ctx:smallCParser.WhileStatementContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#whileBlock.
    def enterWhileBlock(self, ctx:smallCParser.WhileBlockContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#whileBlock.
    def exitWhileBlock(self, ctx:smallCParser.WhileBlockContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#typeName.
    def enterTypeName(self, ctx:smallCParser.TypeNameContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#typeName.
    def exitTypeName(self, ctx:smallCParser.TypeNameContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#declaration.
    def enterDeclaration(self, ctx:smallCParser.DeclarationContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#declaration.
    def exitDeclaration(self, ctx:smallCParser.DeclarationContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#arrayList.
    def enterArrayList(self, ctx:smallCParser.ArrayListContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#arrayList.
    def exitArrayList(self, ctx:smallCParser.ArrayListContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx:smallCParser.FunctionDeclarationContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx:smallCParser.FunctionDeclarationContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#argumentDeclarationList.
    def enterArgumentDeclarationList(self, ctx:smallCParser.ArgumentDeclarationListContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#argumentDeclarationList.
    def exitArgumentDeclarationList(self, ctx:smallCParser.ArgumentDeclarationListContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#functionDefinition.
    def enterFunctionDefinition(self, ctx:smallCParser.FunctionDefinitionContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#functionDefinition.
    def exitFunctionDefinition(self, ctx:smallCParser.FunctionDefinitionContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#returnType.
    def enterReturnType(self, ctx:smallCParser.ReturnTypeContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#returnType.
    def exitReturnType(self, ctx:smallCParser.ReturnTypeContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#arrayElement.
    def enterArrayElement(self, ctx:smallCParser.ArrayElementContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#arrayElement.
    def exitArrayElement(self, ctx:smallCParser.ArrayElementContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#assignment.
    def enterAssignment(self, ctx:smallCParser.AssignmentContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#assignment.
    def exitAssignment(self, ctx:smallCParser.AssignmentContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#intValue.
    def enterIntValue(self, ctx:smallCParser.IntValueContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#intValue.
    def exitIntValue(self, ctx:smallCParser.IntValueContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#floatValue.
    def enterFloatValue(self, ctx:smallCParser.FloatValueContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#floatValue.
    def exitFloatValue(self, ctx:smallCParser.FloatValueContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#charValue.
    def enterCharValue(self, ctx:smallCParser.CharValueContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#charValue.
    def exitCharValue(self, ctx:smallCParser.CharValueContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#functionCall.
    def enterFunctionCall(self, ctx:smallCParser.FunctionCallContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#functionCall.
    def exitFunctionCall(self, ctx:smallCParser.FunctionCallContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#argumentList.
    def enterArgumentList(self, ctx:smallCParser.ArgumentListContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#argumentList.
    def exitArgumentList(self, ctx:smallCParser.ArgumentListContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#comparator.
    def enterComparator(self, ctx:smallCParser.ComparatorContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#comparator.
    def exitComparator(self, ctx:smallCParser.ComparatorContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#operand.
    def enterOperand(self, ctx:smallCParser.OperandContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#operand.
    def exitOperand(self, ctx:smallCParser.OperandContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#sumOperation.
    def enterSumOperation(self, ctx:smallCParser.SumOperationContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#sumOperation.
    def exitSumOperation(self, ctx:smallCParser.SumOperationContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#productOperation.
    def enterProductOperation(self, ctx:smallCParser.ProductOperationContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#productOperation.
    def exitProductOperation(self, ctx:smallCParser.ProductOperationContext):
        popStack(ctx)


    # Enter a parse tree produced by smallCParser#operation.
    def enterOperation(self, ctx:smallCParser.OperationContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#operation.
    def exitOperation(self, ctx:smallCParser.OperationContext):
        popStack(ctx)

    # Enter a parse tree produced by smallCParser#identifier.
    def enterIdentifier(self, ctx:smallCParser.IdentifierContext):
        generateBranch(getRule())

    # Exit a parse tree produced by smallCParser#identifier.
    def exitIdentifier(self, ctx:smallCParser.IdentifierContext):
        popStack(ctx)
