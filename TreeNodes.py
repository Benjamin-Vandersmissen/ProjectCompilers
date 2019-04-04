typename = None

symbolTables = list()

class TreeNode:
    def text(self):
        pass

    def __init__(self):
        self.parent = None
        self.children = []

    def add(self, treenode):
        self.children.append(treenode)
        self.children[-1].parent = self


class SymbolTableNode(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)
        self.symbolTable = dict()

    def addSymbol(self, typename, identifier):
        self.symbolTable[identifier] = typename

    def exists(self, identifier):
        found = identifier in self.symbolTable

        if not found and self.parent is not None:
            return self.parent.exists(identifier)

        return found
class ASTNode(TreeNode):

    def __init__(self):
        TreeNode.__init__(self)
        self.symbolTable = None

    def text(self):
        string = str()
        for child in self.children:
            string += child.text()
        return string

    def buildSymbolTable(self):
        self.startDFS()
        for child in self.children:
            child.buildSymbolTable()

        self.endDFS()

    def startDFS(self):
        #function for overriding in subclasses
        pass

    def endDFS(self):
        pass


class ProgramNode(ASTNode):
    def startDFS(self):
        global symbolTables
        symbolTables.append(SymbolTableNode())
        #TODO: add standaard shit in symboltable

    def endDFS(self):
        self.symbolTable = symbolTables.pop()

class CodeBodyNode(ASTNode):
    def startDFS(self):
        #build a new symbol table
        global symbolTables
        newSymbolTable = SymbolTableNode()
        symbolTables[-1].add(newSymbolTable)
        symbolTables.append(newSymbolTable)

    def endDFS(self):
        #symbol table is finished, pop from stack
        self.symbolTable = symbolTables.pop()

class StatementNode(ASTNode):
    pass

class IfBlockNode(ASTNode):
    pass

class ElseBlockNode(ASTNode):
    pass

class IfStatementNode(ASTNode):
    pass

class WhileStatementNode(ASTNode):
    pass

class WhileBlockNode(ASTNode):
    pass

class TypeNameNode(ASTNode):
    def startDFS(self):
        global typename
        typename = self.children[0].text()

class DeclarationNode(ASTNode):
    pass

class ConstantDeclarationNode(ASTNode):
    pass

class ConstantArrayListNode(ASTNode):
    pass

class ConstantAssignmentNode(ASTNode):
    pass

class ConstantExpressionNode(ASTNode):
    pass

class ConstantSumNode(ASTNode):
    pass

class ConstantProductNode(ASTNode):
    pass

class ConstantNode(ASTNode):
    pass

class ArrayListNode(ASTNode):
    pass

class FunctionDeclarationNode(ASTNode):
    pass

class ArgumentDeclarationListNode(ASTNode):
    pass

class FunctionDefinitionNode(ASTNode):
    pass

class ReturnTypeNode(ASTNode):
    pass

class ArrayElementNode(ASTNode):
    pass

class AssignmentNode(ASTNode):
    pass

class IntValueNode(ASTNode):
    pass

class FloatValueNode(ASTNode):
    pass

class CharValueNode(ASTNode):
    pass

class FunctionCallNode(ASTNode):
    pass

class ArgumentListNode(ASTNode):
    pass

class ComparatorNode(ASTNode):
    pass

class OperandNode(ASTNode):
    pass

class SumOperationNode(ASTNode):
    pass

class ProductOperationNode(ASTNode):
    pass

class OperationNode(ASTNode):
    pass

class IdentifierNode(ASTNode):
    def startDFS(self):
        global typename
        identifier = self.children[0].text()
        if typename is not None:
            symbolTables[-1].addSymbol(typename, identifier)
            typename = None
        else:
            if not symbolTables[-1].exists(identifier):
                print(symbolTables[-1].symbolTable)
                raise Exception("Identifier " + identifier + " not found")

class TokenNode(ASTNode):
    def __init__(self, token):
        ASTNode.__init__(self)
        self.token = token

    def text(self):
        return str(self.token)
