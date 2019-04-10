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



class customListener(smallCListener):

    def generateBranch(self, current,  treeNode):
        global counter


        if current not in counter:
            counter[current] = 0

        self.AST.add(treeNode)
        self.AST = treeNode
        treeNode.id = counter[current]
        counter[current] += 1

        # test = self.AST
        # while test.parent is not None:
        #     test = test.parent
        # file = open("test.dot", "w")
        # test.toDot(file)


    def addTerminalNode(self, node):
        global counter
        token = str(node)

        if token in '{};(),=':  # Negeer deze tokens
            return
        self.AST.processToken(token)

        # self.AST.add(TokenNode(token))

    def popStack(self):

        if len(self.AST.children) == 1 and self.AST.parent is not None:
            self.AST.parent.add(self.AST.children[0])
            self.AST.parent.children.remove(self.AST)

        for child in self.AST.children:
            if self.AST.canMerge(child):
                self.AST.merge(child)

        if self.AST.parent is not None:
            self.AST = self.AST.parent

    def __init__(self):
        self.AST = None

    def visitTerminal(self, node:TerminalNode):
        self.addTerminalNode(node)


    # Enter a parse tree produced by smallCParser#program.
    def enterProgram(self, ctx: smallCParser.ProgramContext):
        global counter
        if self.AST is None:
            self.AST = ProgramNode()
        rule = getRule()
        if rule not in counter:
            counter[rule] = 0
        else:
            counter[rule] += 1

    # Exit a parse tree produced by smallCParser#program.
    def exitProgram(self, ctx: smallCParser.ProgramContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#globalDeclaration.
    def enterGlobalDeclaration(self, ctx: smallCParser.GlobalDeclarationContext):
        # self.generateBranch(getRule(), CodeBodyNode())
        pass

    # Exit a parse tree produced by smallCParser#globalDeclaration.
    def exitGlobalDeclaration(self, ctx: smallCParser.GlobalDeclarationContext):
        # self.popStack(ctx)
        pass

    # Enter a parse tree produced by smallCParser#codeBody.
    def enterCodeBody(self, ctx: smallCParser.CodeBodyContext):
        self.generateBranch(getRule(), CodeBodyNode())

    # Exit a parse tree produced by smallCParser#codeBody.
    def exitCodeBody(self, ctx: smallCParser.CodeBodyContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#statement.
    def enterStatement(self, ctx: smallCParser.StatementContext):
        self.generateBranch(getRule(), StatementNode())

    # Exit a parse tree produced by smallCParser#statement.
    def exitStatement(self, ctx: smallCParser.StatementContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#constantProduct.
    def enterConstantProduct(self, ctx:smallCParser.ConstantProductContext):
        self.generateBranch(getRule(), ConstantProductNode())

    # Exit a parse tree produced by smallCParser#constantProduct.
    def exitConstantProduct(self, ctx:smallCParser.ConstantProductContext):
        self.popStack()


    # Enter a parse tree produced by smallCParser#constantSum.
    def enterConstantSum(self, ctx:smallCParser.ConstantSumContext):
        self.generateBranch(getRule(), ConstantSumNode())

    # Exit a parse tree produced by smallCParser#constantSum.
    def exitConstantSum(self, ctx:smallCParser.ConstantSumContext):
        self.popStack()


    # Enter a parse tree produced by smallCParser#constantComparison.
    def enterConstantComparison(self, ctx:smallCParser.ConstantComparisonContext):
        self.generateBranch(getRule(), ConstantComparisonNode())

    # Exit a parse tree produced by smallCParser#constantComparison.
    def exitConstantComparison(self, ctx:smallCParser.ConstantComparisonContext):
        self.popStack()


    # Enter a parse tree produced by smallCParser#constantValue.
    def enterConstantValue(self, ctx:smallCParser.ConstantValueContext):
        self.generateBranch(getRule(), ConstantValueNode())

    # Exit a parse tree produced by smallCParser#constantValue.
    def exitConstantValue(self, ctx:smallCParser.ConstantValueContext):
        self.popStack()


    # Enter a parse tree produced by smallCParser#product.
    def enterProduct(self, ctx:smallCParser.ProductContext):
        self.generateBranch(getRule(), ProductNode())

    # Exit a parse tree produced by smallCParser#product.
    def exitProduct(self, ctx:smallCParser.ProductContext):
        self.popStack()


    # Enter a parse tree produced by smallCParser#comparison.
    def enterComparison(self, ctx:smallCParser.ComparisonContext):
        self.generateBranch(getRule(), ComparisonNode())

    # Exit a parse tree produced by smallCParser#comparison.
    def exitComparison(self, ctx:smallCParser.ComparisonContext):
        self.popStack()


    # Enter a parse tree produced by smallCParser#sum.
    def enterSum(self, ctx:smallCParser.SumContext):
        self.generateBranch(getRule(), SumNode())

    # Exit a parse tree produced by smallCParser#sum.
    def exitSum(self, ctx:smallCParser.SumContext):
        self.popStack()


    # Enter a parse tree produced by smallCParser#value.
    def enterValue(self, ctx:smallCParser.ValueContext):
        self.generateBranch(getRule(), OperandNode())

    # Exit a parse tree produced by smallCParser#value.
    def exitValue(self, ctx:smallCParser.ValueContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#ifStatement.
    def enterIfStatement(self, ctx: smallCParser.IfStatementContext):
        self.generateBranch(getRule(), IfStatementNode())

    # Exit a parse tree produced by smallCParser#ifStatement.
    def exitIfStatement(self, ctx: smallCParser.IfStatementContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#elseStatement.
    def enterElseStatement(self, ctx: smallCParser.ElseStatementContext):
        self.generateBranch(getRule(), ElseStatementNode())

    # Exit a parse tree produced by smallCParser#elseStatement.
    def exitElseStatement(self, ctx: smallCParser.ElseStatementContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#whileStatement.
    def enterWhileStatement(self, ctx: smallCParser.WhileStatementContext):
        self.generateBranch(getRule(), WhileStatementNode())

    # Exit a parse tree produced by smallCParser#whileStatement.
    def exitWhileStatement(self, ctx: smallCParser.WhileStatementContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#typeName.
    def enterTypeName(self, ctx: smallCParser.TypeNameContext):
        self.generateBranch(getRule(), TypeNameNode())

    # Exit a parse tree produced by smallCParser#typeName.
    def exitTypeName(self, ctx: smallCParser.TypeNameContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#declaration.
    def enterDeclaration(self, ctx: smallCParser.DeclarationContext):
        self.generateBranch(getRule(), DeclarationNode())

    # Exit a parse tree produced by smallCParser#declaration.
    def exitDeclaration(self, ctx: smallCParser.DeclarationContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#constantDeclaration.
    def enterConstantDeclaration(self, ctx: smallCParser.ConstantDeclarationContext):
        self.generateBranch(getRule(), ConstantDeclarationNode())

    # Exit a parse tree produced by smallCParser#constantDeclaration.
    def exitConstantDeclaration(self, ctx: smallCParser.ConstantDeclarationContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#arrayList.
    def enterArrayList(self, ctx: smallCParser.ArrayListContext):
        self.generateBranch(getRule(), ArrayListNode())

    # Exit a parse tree produced by smallCParser#arrayList.
    def exitArrayList(self, ctx: smallCParser.ArrayListContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#constantArrayList.
    def enterConstantArrayList(self, ctx: smallCParser.ConstantArrayListContext):
        self.generateBranch(getRule(), ConstantArrayListNode())

    # Exit a parse tree produced by smallCParser#constantArrayList.
    def exitConstantArrayList(self, ctx: smallCParser.ConstantArrayListContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#argumentDeclarationList.
    def enterArgumentDeclarationList(self, ctx: smallCParser.ArgumentDeclarationListContext):
        self.generateBranch(getRule(), ArgumentDeclarationListNode())

    # Exit a parse tree produced by smallCParser#argumentDeclarationList.
    def exitArgumentDeclarationList(self, ctx: smallCParser.ArgumentDeclarationListContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx: smallCParser.FunctionDeclarationContext):
        self.generateBranch(getRule(), FunctionDeclarationNode())

    # Exit a parse tree produced by smallCParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx: smallCParser.FunctionDeclarationContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#functionDefinition.
    def enterFunctionDefinition(self, ctx: smallCParser.FunctionDefinitionContext):
        self.generateBranch(getRule(), FunctionDefinitionNode())

    # Exit a parse tree produced by smallCParser#functionDefinition.
    def exitFunctionDefinition(self, ctx: smallCParser.FunctionDefinitionContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#returnType.
    def enterReturnType(self, ctx: smallCParser.ReturnTypeContext):
        self.generateBranch(getRule(), ReturnTypeNode())

    # Exit a parse tree produced by smallCParser#returnType.
    def exitReturnType(self, ctx: smallCParser.ReturnTypeContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#arrayElement.
    def enterArrayElement(self, ctx: smallCParser.ArrayElementContext):
        self.generateBranch(getRule(), ArrayElementNode())

    # Exit a parse tree produced by smallCParser#arrayElement.
    def exitArrayElement(self, ctx: smallCParser.ArrayElementContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#assignment.
    def enterAssignment(self, ctx: smallCParser.AssignmentContext):
        self.generateBranch(getRule(), AssignmentNode())

    # Exit a parse tree produced by smallCParser#assignment.
    def exitAssignment(self, ctx: smallCParser.AssignmentContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#constantAssignment.
    def enterConstantAssignment(self, ctx: smallCParser.ConstantAssignmentContext):
        self.generateBranch(getRule(), ConstantAssignmentNode())

    # Exit a parse tree produced by smallCParser#constantAssignment.
    def exitConstantAssignment(self, ctx: smallCParser.ConstantAssignmentContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#functionCall.
    def enterFunctionCall(self, ctx: smallCParser.FunctionCallContext):
        self.generateBranch(getRule(), FunctionCallNode())

    # Exit a parse tree produced by smallCParser#functionCall.
    def exitFunctionCall(self, ctx: smallCParser.FunctionCallContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#argumentList.
    def enterArgumentList(self, ctx: smallCParser.ArgumentListContext):
        self.generateBranch(getRule(), ArgumentListNode())

    # Exit a parse tree produced by smallCParser#argumentList.
    def exitArgumentList(self, ctx: smallCParser.ArgumentListContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#operand.
    def enterOperand(self, ctx: smallCParser.OperandContext):
        self.generateBranch(getRule(), OperandNode())

    # Exit a parse tree produced by smallCParser#operand.
    def exitOperand(self, ctx: smallCParser.OperandContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#constant.
    def enterConstant(self, ctx: smallCParser.ConstantContext):
        self.generateBranch(getRule(), ConstantNode())

    # Exit a parse tree produced by smallCParser#constant.
    def exitConstant(self, ctx: smallCParser.ConstantContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#identifier.
    def enterIdentifier(self, ctx: smallCParser.IdentifierContext):
        self.generateBranch(getRule(), IdentifierNode())

    # Exit a parse tree produced by smallCParser#identifier.
    def exitIdentifier(self, ctx: smallCParser.IdentifierContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#intValue.
    def enterIntValue(self, ctx: smallCParser.IntValueContext):
        self.generateBranch(getRule(), IntValueNode())

    # Exit a parse tree produced by smallCParser#intValue.
    def exitIntValue(self, ctx: smallCParser.IntValueContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#floatValue.
    def enterFloatValue(self, ctx: smallCParser.FloatValueContext):
        self.generateBranch(getRule(), FloatValueNode())

    # Exit a parse tree produced by smallCParser#floatValue.
    def exitFloatValue(self, ctx: smallCParser.FloatValueContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#charValue.
    def enterCharValue(self, ctx: smallCParser.CharValueContext):
        self.generateBranch(getRule(), CharValueNode())

    # Exit a parse tree produced by smallCParser#charValue.
    def exitCharValue(self, ctx: smallCParser.CharValueContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#dereference.
    def enterDereference(self, ctx: smallCParser.DereferenceContext):
        self.generateBranch(getRule(), DereferenceNode())

    # Exit a parse tree produced by smallCParser#dereference.
    def exitDereference(self, ctx: smallCParser.DereferenceContext):
        self.popStack()

    # Enter a parse tree produced by smallCParser#depointer.
    def enterDepointer(self, ctx: smallCParser.DepointerContext):
        self.generateBranch(getRule(), DepointerNode())

    # Exit a parse tree produced by smallCParser#depointer.
    def exitDepointer(self, ctx: smallCParser.DepointerContext):
        self.popStack()
