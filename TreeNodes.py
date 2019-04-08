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

    def dotRepresentation(self):
        representation = 'symboltable" [shape="plaintext" label=< <table>\n'

        representation += "<th><td><b>identifier</b></td><td><b>type</b></td></th>"

        for key, value in self.symbolTable.items():
            representation += '\n<tr><td>' + key + '</td><td>' + value + '</td></tr>'

        representation += '</table>>];\n'

        return representation

class ASTNode(TreeNode):

    def __init__(self):
        TreeNode.__init__(self)
        self.symbolTable = None
        self.id = 0

    def name(self):
        return self.__class__.__name__.split('Node')[0]

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


    def toDot(self, file):
        if self.parent is None:
            file.write("digraph AST {\n")
            file.write('\t"' + self.name() + '_' + str(self.id) + '"[label="'+self.name() + '"];\n')
        else:
            file.write('\t"' + self.name() + '_' + str(self.id) + '"[label="'+self.name() + '"];\n')
            file.write('\t"' + self.parent.name() + '_' + str(self.parent.id) + '" -> "' + self.name() + '_' + str(self.id) + '";\n')

        if self.symbolTable:
            file.write('\t"' + self.name() + '_' + str(self.id) + '_' + self.symbolTable.dotRepresentation())
            file.write('\t"' + self.name() + '_' + str(self.id) + '"->"' + self.name() + '_' + str(self.id) +
                       '_symboltable" [style="dotted"];\n')

        for child in self.children:
            child.toDot(file)
        if self.parent is None:
            file.write("}")

    def processToken(self, token):
        # empty function to be overridden in derived classes
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

class DereferenceNode(ASTNode):
    pass

class DepointerNode(ASTNode):
    pass

class ElseStatementNode(ASTNode):
    pass

class IfStatementNode(ASTNode):
    pass

class WhileStatementNode(ASTNode):
    pass

class WhileBlockNode(ASTNode):
    pass

class TypeNameNode(ASTNode):

    def __init__(self):
        ASTNode.__init__(self)
        self.typename = ''

    def processToken(self, token):
        self.typename += token

    def startDFS(self):
        global typename
        typename = self.typename

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
    def __init__(self):
        ASTNode.__init__(self)
        self.value = None

    def processToken(self, token):
        self.value = int(token)

class FloatValueNode(ASTNode):
    def __init__(self):
        ASTNode.__init__(self)
        self.value = None

    def processToken(self, token):
        self.value = float(token)

class CharValueNode(ASTNode):
    def __init__(self):
        ASTNode.__init__(self)
        self.value = None

    def processToken(self, token):
        self.value = token

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

class ExpressionNode(ASTNode):
    def __init__(self):
        ASTNode.__init__(self)
        self.operators = []

    def processToken(self, token):
        self.operators.append(token)

class IdentifierNode(ASTNode):

    def __init__(self):
        ASTNode.__init__(self)
        self.identifier = ''

    def processToken(self, token):
        self.identifier = token

    def startDFS(self):
        global typename
        if typename is not None:
            symbolTables[-1].addSymbol(typename, self.identifier)
            typename = None
        else:
            if not symbolTables[-1].exists(self.identifier):
                print(symbolTables[-1].symbolTable)
                raise Exception("Identifier " + self.identifier + " not found")

class TokenNode(ASTNode):
    def __init__(self, token):
        ASTNode.__init__(self)
        self.token = token

    def text(self):
        return str(self.token)
