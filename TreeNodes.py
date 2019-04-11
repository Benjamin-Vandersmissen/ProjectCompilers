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

    def getEntry(self, index):
        return list(self.symbolTable.items())[index]

class FunctionTableNode(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)
        self.functionTable = dict()

    def addFunction(self, returnType, identifier, arguments, defined=False):
        self.functionTable[identifier] = (returnType, arguments, defined)

    def exists(self, identifier):
        found = identifier in self.functionTable

        if not found and self.parent is not None:
            return self.parent.exists(identifier)

        return found

    def signatureExists(self, returnType, identifier, arguments):
        if identifier in self.functionTable:
            value = self.functionTable[identifier]
            return returnType == value[0] and arguments == value[1]
        return False

    def dotRepresentation(self):
        representation = 'functiontable" [shape="plaintext" label=< <table>\n'

        representation += "<th><td><b>identifier</b></td><td><b>returnType</b></td>" \
                          "<td><b>arguments</b></td><td><b>defined</b></td></th>"

        for key, value in self.functionTable.items():
            representation += '\n<tr><td>' + key + '</td><td>' + value[0] + '</td>'

            arguments = ''
            for argument in value[1]:
                arguments += argument + ', '
            if len(arguments) > 2 and arguments[-2] == ',':
                arguments = arguments[:-2]

            representation += '<td>' + arguments + '</td><td>' + str(value[2]) + '</td></tr>'

        representation += '</table>>];\n'
        return representation

    def isDefined(self, identifier):
        if identifier in self.functionTable:
            return self.functionTable[identifier][2]
        else:
            return False

functionTable = FunctionTableNode()

class ASTNode(TreeNode):

    def __init__(self):
        TreeNode.__init__(self)
        self.symbolTable = None
        self.functionTable = None
        self.id = 0
        self.line = 0
        self.column = 0

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

    def canMerge(self, node):
        return node.__class__ == self.__class__

    def merge(self, node):
        node.parent.children.remove(node)
        for child in node.children:
            self.add(child)


    def startDFS(self):
        #function for overriding in subclasses
        pass

    def endDFS(self):
        pass


    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="'+self.name() + '"];\n'

    def toDot(self, file):
        if self.parent is None:
            file.write("digraph AST {\n")
            file.write(self.dotRepresentation())
        else:
            file.write(self.dotRepresentation())
            file.write('\t"' + self.parent.name() + '_' + str(self.parent.id) + '" -> "' + self.name() + '_' + str(self.id) + '";\n')

        if self.symbolTable:
            file.write('\t"' + self.name() + '_' + str(self.id) + '_' + self.symbolTable.dotRepresentation())
            file.write('\t"' + self.name() + '_' + str(self.id) + '"->"' + self.name() + '_' + str(self.id) +
                       '_symboltable" [style="dotted"];\n')

        if self.functionTable:
            file.write('\t"' + self.name() + '_' + str(self.id) + '_' + self.functionTable.dotRepresentation())
            file.write('\t"' + self.name() + '_' + str(self.id) + '"->"' + self.name() + '_' + str(self.id) +
                       '_functiontable" [style="dotted"];\n')

        for child in self.children:
            child.toDot(file)
        if self.parent is None:
            file.write("}")

    def toLLVM(self, file):
        #LLVM output here
        for child in self.children:
            child.toLLVM(file)

    def processToken(self, token):
        # empty function to be overridden in derived classes
        pass

class ProgramNode(ASTNode):
    def startDFS(self):
        global symbolTables
        symbolTables.append(SymbolTableNode())
        #TODO: add standaard shit in symboltable

    def endDFS(self):
        global symbolTables, functionTable
        self.symbolTable = symbolTables.pop()
        self.functionTable = functionTable

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

class ReturnStatementNode(ASTNode):
    pass

class DereferenceNode(ASTNode):
    def __init__(self):
        ASTNode.__init__(self)
        self.dereference = ''

    def processToken(self, token):
        self.dereference += token

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.dereference + '"];\n'

class DepointerNode(ASTNode):
    def __init__(self):
        ASTNode.__init__(self)
        self.depointer = ''

    def processToken(self, token):
        self.depointer += token

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.depointer + '"];\n'

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

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.typename + '"];\n'

class DeclarationNode(ASTNode):
    def startDFS(self):
        typename = self.children[0].typename
        identifier = self.children[1].identifier
        symbolTables[-1].addSymbol(typename, identifier)

class ArrayDeclarationNode(ASTNode):
    def __init__(self):
        ASTNode.__init__(self)

    def startDFS(self):
        typename = self.children[0].typename
        identifier = self.children[1].identifier
        size = ' '
        if len(self.children) == 4:
            size = self.children[2].value
        if len(self.children) == 3:
            if isinstance(self.children[2], ArrayListNode):
                size = len(self.children[2])
            else:
                size = self.children[2].value
        typename = typename + '[' + str(size) + ']'

        symbolTables[-1].addSymbol(typename, identifier)


class ConstantDeclarationNode(DeclarationNode):
    def startDFS(self):
        typename = self.children[0].typename
        if isinstance(self.children[1], IdentifierNode):
            identifier = self.children[1].identifier
        else:
            identifier = self.children[1].children[0].identifier
        symbolTables[-1].addSymbol(typename, identifier)

class ConstantArrayDeclarationNode(ArrayDeclarationNode):
    pass

class ConstantArrayListNode(ASTNode):
    pass

class ConstantAssignmentNode(ASTNode):
    pass

class ConstantExpressionNode(ASTNode):
    pass

class ConstantValueNode(ASTNode):
    pass

class ConstantNode(ASTNode):
    pass

class ArrayListNode(ASTNode):
    pass

class FunctionDeclarationNode(ASTNode):
    def startDFS(self):
        # build a new symbol table
        global symbolTables
        newSymbolTable = SymbolTableNode()
        symbolTables[-1].add(newSymbolTable)
        symbolTables.append(newSymbolTable)

        typename = self.children[0].typename
        identifier = self.children[1].identifier

        arguments = list()
        if len(self.children) > 2:
            for i in range(0, len(self.children[2].children), 2):
                argumentType = self.children[2].children[i].typename
                arguments.append(argumentType)

        if functionTable.exists(identifier) and not functionTable.signatureExists(typename, identifier, arguments):
            raise Exception("function " + identifier + " is redeclared at "+str(self.line)+":"+str(self.column)+" with a different signature")

        functionTable.addFunction(typename, identifier, list(), False)

    def endDFS(self):
        # symbol table is finished, pop from stack
        self.symbolTable = symbolTables.pop()

        typename = self.children[0].typename
        identifier = self.children[1].identifier

        arguments = list()
        for i in range(1, len(self.symbolTable.symbolTable)):
            arguments.append(self.symbolTable.getEntry(i)[1])

        functionTable.addFunction(typename, identifier, arguments, False)

        # This is a function declaration in a function definition
        # We need to push all symbolTable entries back a level
        if len(symbolTables) > 1:
            symbolTables[-1] = self.symbolTable
        self.symbolTable = None

class ArgumentDeclarationListNode(ASTNode):
    def startDFS(self):
        for i in range(0, len(self.children), 2):
            typename = self.children[i].typename
            identifier = self.children[i+1].identifier
            symbolTables[-1].addSymbol(typename, identifier)

class FunctionDefinitionNode(ASTNode):
    def startDFS(self):
        # build a new symbol table

        identifier = self.children[0].children[1].identifier

        if functionTable.isDefined(identifier):
            raise Exception("Redefinition of function " + identifier+" at " + str(self.line)+":"+str(self.column))
        global symbolTables
        newSymbolTable = SymbolTableNode()
        symbolTables[-1].add(newSymbolTable)
        symbolTables.append(newSymbolTable)

    def endDFS(self):
        # symbol table is finished, pop from stack
        self.symbolTable = symbolTables.pop()

        typename = self.children[0].children[0].typename  # declaration is always first child of definition
        identifier = self.children[0].children[1].identifier

        arguments = list()
        for i in range(0, len(self.symbolTable.symbolTable)):
            arguments.append(self.symbolTable.getEntry(i)[1])

        functionTable.addFunction(typename, identifier, arguments, True)

class ReturnTypeNode(TypeNameNode):
    pass

class ArrayElementNode(ASTNode):
    pass

class AssignmentNode(ASTNode):
    pass

class ValueNode(ASTNode):
    def __init__(self):
        ASTNode.__init__(self)
        self.value = None

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + str(self.value) + '"];\n'


class IntValueNode(ValueNode):

    def __init__(self):
        ValueNode.__init__(self)
        self.sign = 1

    def processToken(self, token):
        if token == '+':
            return
        elif token == '-':
            self.sign *= -1
            return
        self.value = int(token)

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + \
               ('-' if self.sign < 0 else '') + str(self.value) + '"];\n'

class FloatValueNode(ValueNode):

    def __init__(self):
        ValueNode.__init__(self)
        self.sign = 1
        self.integer = None
        self.fraction = None

    def processToken(self, token):
        if token == '+':
            return
        elif token == '-':
            self.sign *= -1
            return
        elif token == '.':
            return

        if self.integer is None:
            self.integer = int(token)
        else:
            self.fraction = int(token)
            self.value = float(str(self.integer)+'.'+str(self.fraction))

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + \
               ('-' if self.sign < 0 else '') + str(self.value) + '"];\n'

class CharValueNode(ValueNode):

    def processToken(self, token):
        self.value = token

class FunctionCallNode(ASTNode):
    def startDFS(self):
        identifier = self.children[0].identifier
        if not functionTable.exists(identifier):
            raise Exception("Identifier " + identifier + " not found at " + str(self.line)+":"+str(self.column))
        if not functionTable.isDefined(identifier):
            raise Exception("Function " + identifier + " is not defined at " + str(self.line)+":"+str(self.column))
        # TODO: Typecheck each argument and add argument count check

class ArgumentListNode(ASTNode):
    pass

class OperandNode(ASTNode):
    pass

class OperationNode(ASTNode):
    def __init__(self):
        ASTNode.__init__(self)
        self.operator = None

    def processToken(self, token):
        self.operator = token

    def canMerge(self, node):
        return ASTNode.canMerge(self, node) and node.operator == self.operator

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.operator + '"];\n'

class SumNode(OperationNode):
    pass

class ProductNode(OperationNode):
    pass

class ComparisonNode(OperationNode):
    pass

class ConstantComparisonNode(OperationNode):
    pass

class ConstantSumNode(OperationNode):
    pass

class ConstantProductNode(OperationNode):
    pass

class IdentifierNode(ASTNode):

    def __init__(self):
        ASTNode.__init__(self)
        self.identifier = ''

    def processToken(self, token):
        self.identifier = token

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.identifier + '"];\n'

    def startDFS(self):
        if not symbolTables[-1].exists(self.identifier) and not functionTable.exists(self.identifier):
            print(symbolTables[-1].symbolTable)
            raise Exception("Identifier " + self.identifier + " not found at " + str(self.line)+":"+str(self.column))

