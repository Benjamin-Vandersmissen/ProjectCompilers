from smallCListener import smallCListener
from smallCParser import smallCParser
from antlr4 import TerminalNode
from TreeNodes import *


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



class customListener(smallCListener):

    def generateBranch(self, current,  treeNode):
        global counter, stack, file

        pair = stack[-1]

        if current not in counter:
            counter[current] = 0

        if current != pair[0]:
            self.AST.add(treeNode)
            self.AST = treeNode
            treeNode.id = counter[current]
            stack.append((current, counter[current]))
            counter[current] += 1
        elif current == pair[0]:
            stack.append(stack[-1])

    def addTerminalNode(self, node):
        global stack, tokens
        pair = stack[-1]
        token = str(node)

        self.AST.add(TokenNode(token))

        if token in '{};(),=':  # Negeer deze tokens
            return
        if token not in tokens:
            tokens[token] = 0
        else:
            tokens[token] += 1

        # file.write('\t"' + pair[0] + '_' + str(pair[1]) + '"-> "TOKEN_' +
        #            token + '_' + str(tokens[token]) + '" [style=dotted];\n')
        # file.write('\t"TOKEN_' + token + '_' + str(tokens[token]) + '" [shape=plaintext];\n')

    def popStack(self,context):
        global stack, tokens
        pair = stack[-1]
        stack = stack[:-1]

        if len(stack) == 0:
            # file.write('\n}')
            print(self.AST.text())
            self.AST.buildSymbolTable()
        elif pair != stack[-1]:

            if len(self.AST.children) == 1 and not isinstance(self.AST.children[0], TokenNode) and self.AST.parent is not None:
                self.AST.parent.add(self.AST.children[0])
                self.AST.parent.children.remove(self.AST)
            self.AST = self.AST.parent

    def __init__(self):
        self.AST = None

    def visitTerminal(self, node:TerminalNode):
        self.addTerminalNode(node)

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
        if self.AST is None:
            self.AST = ProgramNode()
        rule = getRule()
        if rule not in counter:
            counter[rule] = 0
            # file.write("digraph AST {\n")
            stack.append((rule, 0))
        else:
            counter[rule] += 1
            stack.append((rule, 0))


    # Exit a parse tree produced by smallCParser#program.
    def exitProgram(self, ctx:smallCParser.ProgramContext):
        global file
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack(ctx)

    # Enter a parse tree produced by smallCParser#codeBody.
    def enterCodeBody(self, ctx:smallCParser.CodeBodyContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),CodeBodyNode())

    # Exit a parse tree produced by smallCParser#codeBody.
    def exitCodeBody(self, ctx:smallCParser.CodeBodyContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#statement.
    def enterStatement(self, ctx:smallCParser.StatementContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),StatementNode())

    # Exit a parse tree produced by smallCParser#statement.
    def exitStatement(self, ctx:smallCParser.StatementContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#ifBlock.
    def enterIfBlock(self, ctx:smallCParser.IfBlockContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),IfBlockNode())

    # Exit a parse tree produced by smallCParser#ifBlock.
    def exitIfBlock(self, ctx:smallCParser.IfBlockContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#elseBlock.
    def enterElseBlock(self, ctx:smallCParser.ElseBlockContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),ElseBlockNode())

    # Exit a parse tree produced by smallCParser#elseBlock.
    def exitElseBlock(self, ctx:smallCParser.ElseBlockContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#ifStatement.
    def enterIfStatement(self, ctx:smallCParser.IfStatementContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),IfStatementNode())

    # Exit a parse tree produced by smallCParser#ifStatement.
    def exitIfStatement(self, ctx:smallCParser.IfStatementContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#whileStatement.
    def enterWhileStatement(self, ctx:smallCParser.WhileStatementContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),WhileStatementNode())

    # Exit a parse tree produced by smallCParser#whileStatement.
    def exitWhileStatement(self, ctx:smallCParser.WhileStatementContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#whileBlock.
    def enterWhileBlock(self, ctx:smallCParser.WhileBlockContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),WhileBlockNode())

    # Exit a parse tree produced by smallCParser#whileBlock.
    def exitWhileBlock(self, ctx:smallCParser.WhileBlockContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#typeName.
    def enterTypeName(self, ctx:smallCParser.TypeNameContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),TypeNameNode())

    # Exit a parse tree produced by smallCParser#typeName.
    def exitTypeName(self, ctx:smallCParser.TypeNameContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#declaration.
    def enterDeclaration(self, ctx:smallCParser.DeclarationContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),DeclarationNode())

    # Exit a parse tree produced by smallCParser#declaration.
    def exitDeclaration(self, ctx:smallCParser.DeclarationContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)

        # Enter a parse tree produced by smallCParser#constantDeclaration.
    def enterConstantDeclaration(self, ctx: smallCParser.ConstantDeclarationContext):
        self.generateBranch(getRule(),ConstantDeclarationNode())

        # Exit a parse tree produced by smallCParser#constantDeclaration.
    def exitConstantDeclaration(self, ctx: smallCParser.ConstantDeclarationContext):
        self.popStack( ctx)

        # Enter a parse tree produced by smallCParser#constantArrayList.
    def enterConstantArrayList(self, ctx: smallCParser.ConstantArrayListContext):
        self.generateBranch(getRule(),ConstantArrayListNode())

    # Exit a parse tree produced by smallCParser#constantArrayList.
    def exitConstantArrayList(self, ctx: smallCParser.ConstantArrayListContext):
        self.popStack( ctx)

    # Enter a parse tree produced by smallCParser#constantAssignment.
    def enterConstantAssignment(self, ctx: smallCParser.ConstantAssignmentContext):
        self.generateBranch(getRule(),ConstantAssignmentNode())

    # Exit a parse tree produced by smallCParser#constantAssignment.
    def exitConstantAssignment(self, ctx: smallCParser.ConstantAssignmentContext):
        self.popStack( ctx)

    # Enter a parse tree produced by smallCParser#constantExpression.
    def enterConstantExpression(self, ctx: smallCParser.ConstantExpressionContext):
        self.generateBranch(getRule(),ConstantExpressionNode())

    # Exit a parse tree produced by smallCParser#constantExpression.
    def exitConstantExpression(self, ctx: smallCParser.ConstantExpressionContext):
        self.popStack( ctx)

    # Enter a parse tree produced by smallCParser#constantSum.
    def enterConstantSum(self, ctx: smallCParser.ConstantSumContext):
        self.generateBranch(getRule(),ConstantSumNode())

    # Exit a parse tree produced by smallCParser#constantSum.
    def exitConstantSum(self, ctx: smallCParser.ConstantSumContext):
        self.popStack( ctx)

    # Enter a parse tree produced by smallCParser#constantProduct.
    def enterConstantProduct(self, ctx: smallCParser.ConstantProductContext):
        self.generateBranch(getRule(),ConstantProductNode())

    # Exit a parse tree produced by smallCParser#constantProduct.
    def exitConstantProduct(self, ctx: smallCParser.ConstantProductContext):
        self.popStack( ctx)

    # Enter a parse tree produced by smallCParser#constant.
    def enterConstant(self, ctx: smallCParser.ConstantContext):
        self.generateBranch(getRule(),ConstantNode())

    # Exit a parse tree produced by smallCParser#constant.
    def exitConstant(self, ctx: smallCParser.ConstantContext):
        self.popStack( ctx)

    # Enter a parse tree produced by smallCParser#arrayList.
    def enterArrayList(self, ctx:smallCParser.ArrayListContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),ArrayListNode())

    # Exit a parse tree produced by smallCParser#arrayList.
    def exitArrayList(self, ctx:smallCParser.ArrayListContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx:smallCParser.FunctionDeclarationContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),FunctionDeclarationNode())

    # Exit a parse tree produced by smallCParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx:smallCParser.FunctionDeclarationContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#argumentDeclarationList.
    def enterArgumentDeclarationList(self, ctx:smallCParser.ArgumentDeclarationListContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),ArgumentDeclarationListNode())

    # Exit a parse tree produced by smallCParser#argumentDeclarationList.
    def exitArgumentDeclarationList(self, ctx:smallCParser.ArgumentDeclarationListContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#functionDefinition.
    def enterFunctionDefinition(self, ctx:smallCParser.FunctionDefinitionContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),FunctionDefinitionNode())

    # Exit a parse tree produced by smallCParser#functionDefinition.
    def exitFunctionDefinition(self, ctx:smallCParser.FunctionDefinitionContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#returnType.
    def enterReturnType(self, ctx:smallCParser.ReturnTypeContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),ReturnTypeNode())

    # Exit a parse tree produced by smallCParser#returnType.
    def exitReturnType(self, ctx:smallCParser.ReturnTypeContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#arrayElement.
    def enterArrayElement(self, ctx:smallCParser.ArrayElementContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),ArrayElementNode())

    # Exit a parse tree produced by smallCParser#arrayElement.
    def exitArrayElement(self, ctx:smallCParser.ArrayElementContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#assignment.
    def enterAssignment(self, ctx:smallCParser.AssignmentContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),AssignmentNode())

    # Exit a parse tree produced by smallCParser#assignment.
    def exitAssignment(self, ctx:smallCParser.AssignmentContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#intValue.
    def enterIntValue(self, ctx:smallCParser.IntValueContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),IntValueNode())

    # Exit a parse tree produced by smallCParser#intValue.
    def exitIntValue(self, ctx:smallCParser.IntValueContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#floatValue.
    def enterFloatValue(self, ctx:smallCParser.FloatValueContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),FloatValueNode())

    # Exit a parse tree produced by smallCParser#floatValue.
    def exitFloatValue(self, ctx:smallCParser.FloatValueContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#charValue.
    def enterCharValue(self, ctx:smallCParser.CharValueContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),CharValueNode())

    # Exit a parse tree produced by smallCParser#charValue.
    def exitCharValue(self, ctx:smallCParser.CharValueContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#functionCall.
    def enterFunctionCall(self, ctx:smallCParser.FunctionCallContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),FunctionCallNode())

    # Exit a parse tree produced by smallCParser#functionCall.
    def exitFunctionCall(self, ctx:smallCParser.FunctionCallContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#argumentList.
    def enterArgumentList(self, ctx:smallCParser.ArgumentListContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),ArrayListNode())

    # Exit a parse tree produced by smallCParser#argumentList.
    def exitArgumentList(self, ctx:smallCParser.ArgumentListContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#comparator.
    def enterComparator(self, ctx:smallCParser.ComparatorContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),ComparatorNode())

    # Exit a parse tree produced by smallCParser#comparator.
    def exitComparator(self, ctx:smallCParser.ComparatorContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#operand.
    def enterOperand(self, ctx:smallCParser.OperandContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),OperandNode())

    # Exit a parse tree produced by smallCParser#operand.
    def exitOperand(self, ctx:smallCParser.OperandContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#sumOperation.
    def enterSumOperation(self, ctx:smallCParser.SumOperationContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),SumOperationNode())

    # Exit a parse tree produced by smallCParser#sumOperation.
    def exitSumOperation(self, ctx:smallCParser.SumOperationContext):
        ##print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#productOperation.
    def enterProductOperation(self, ctx:smallCParser.ProductOperationContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),ProductOperationNode())

    # Exit a parse tree produced by smallCParser#productOperation.
    def exitProductOperation(self, ctx:smallCParser.ProductOperationContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)


    # Enter a parse tree produced by smallCParser#operation.
    def enterOperation(self, ctx:smallCParser.OperationContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),OperationNode())

    # Exit a parse tree produced by smallCParser#operation.
    def exitOperation(self, ctx:smallCParser.OperationContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)

    # Enter a parse tree produced by smallCParser#identifier.
    def enterIdentifier(self, ctx:smallCParser.IdentifierContext):
        #print("Enter: ", getRule(), ctx.getText())
        self.generateBranch(getRule(),IdentifierNode())

    # Exit a parse tree produced by smallCParser#identifier.
    def exitIdentifier(self, ctx:smallCParser.IdentifierContext):
        #print("Leave: ", getRule(), ctx.getText())
        self.popStack( ctx)
