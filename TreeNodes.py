import llvm
import copy

symbolTables = list()
reservedWords = ['if', 'else', 'return', 'while', 'char', 'int', 'float', 'void']
labelCounter = 0


class TreeNode:
    def text(self):
        pass

    def __init__(self):
        self.parent = None
        self.children = []

    # Add a childnode
    def add(self, treenode):
        self.children.append(treenode)
        self.children[-1].parent = self

    # Add a childnode in front of the nodes
    def addFront(self, treenode):
        self.children.insert(0, treenode)
        self.children[0].parent = self


class SymbolTableNode(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)
        self.symbolTable = dict()

    # Add a symbol (typename and identifier) in the symboltable
    def addSymbol(self, typename, identifier):
        self.symbolTable[identifier] = typename

    # Check if a symbol exists in this or this ancestors scopes
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

    # Get the entry for a specific identifier (returns the type)
    # Returns None if the entry is not found in this or this ancestors scope
    def getEntry(self, identifier):
        found = identifier in self.symbolTable

        if not found and self.parent is not None:
            return self.parent.getEntry(identifier)
        elif found:
            return self.symbolTable[identifier]

        return None


class FunctionTableNode(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)
        self.functionTable = dict()

    # Add a function (returnType, identifier, list of argument types) to the function table
    def addFunction(self, returnType, identifier, arguments, defined=False):
        self.functionTable[identifier] = (returnType, arguments, defined)

    # Check if an identifier exists in the function table
    def exists(self, identifier):
        found = identifier in self.functionTable

        if not found and self.parent is not None:
            return self.parent.exists(identifier)

        return found

    # Check if a signature (returnType, identifier, list of argumentTypes) exists in the function table
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

    # Check if a function with given identifier is defined
    def isDefined(self, identifier):
        if identifier in self.functionTable:
            return self.functionTable[identifier][2]
        else:
            return False


functionTable = FunctionTableNode()


class ASTNode(TreeNode):
    count = 0

    def __init__(self):
        TreeNode.__init__(self)
        self.symbolTable = None
        self.functionTable = None
        self.id = type(self).count
        type(self).count += 1
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
        index = 0
        while index < len(self.children):
            child = self.children[index]
            child.buildSymbolTable()
            if child in self.children:  # child is not removed => update index
                index += 1

        self.endDFS()

    # Check if two nodes in the AST can merge
    def canMerge(self, node):
        return node.__class__ == self.__class__

    # Merge a node with this node
    def merge(self, node):
        node.parent.children.remove(node)
        self.children = node.children + self.children
        for child in node.children:
            child.parent = self

    def startDFS(self):
        # function for overriding in subclasses
        pass

    def endDFS(self):
        pass

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.name() + '"];\n'

    def toDot(self, file):
        if self.parent is None:
            file.write("digraph AST {\n")
            file.write(self.dotRepresentation())
        else:
            file.write(self.dotRepresentation())
            file.write('\t"' + self.parent.name() + '_' + str(self.parent.id) + '" -> "' + self.name() + '_' + str(
                self.id) + '";\n')

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

    # Create the llvm code for this node in the AST and if asked in a certain type
    # expects file to be an opened writable file
    # expects funcDef to be a FunctionDefinitionNode. Only children of such a node need this argument!!
    # expects codeBody to be a CodeBodyNode. Only children of such a node need this argument!
    # expects returnType to be an llvm typename. Only nodes that return a value or variable can use this argument!
    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        # LLVM output part 1 here
        for child in self.children:
            child.toLLVM(file)
        # LLVM output part 2 here

    def processToken(self, token):
        # empty function to be overridden in derived classes
        pass

    def throwError(self, text):
        raise Exception("({}:{}) : ".format(self.line, self.column) + text)

    def printWarning(self, text):
        print("Warning ({}:{}) : ".format(self.line, self.column) + text)


class ProgramNode(ASTNode):
    def __init__(self):
        ASTNode.__init__(self)
        self.useSTDIO = False
        self.typeAndAlignTable = dict()

    def startDFS(self):
        if self.useSTDIO:
            functionTable.addFunction('int', 'printf', ['char*', '...'], True)
            functionTable.addFunction('int', 'scanf', ['char*', '...'], True)

        global symbolTables
        symbolTables.append(SymbolTableNode())

    def endDFS(self):
        global symbolTables, functionTable
        self.symbolTable = symbolTables.pop()
        self.functionTable = functionTable

        # Optimise global assignments and declarations, by only executing the last global assignment for a variable

        # Find each global declaration
        declarations = dict()
        for child in self.children:
            if isinstance(child, ConstantDeclarationNode):
                if isinstance(child.children[1], IdentifierNode):
                    declarations[child.children[1].identifier] = child
                else:
                    declarations[child.children[1].children[0].identifier] = child

        # Find the last assignment for each global variable
        for child in reversed(self.children):
            if isinstance(child, ConstantAssignmentNode):
                identifier = child.children[0].identifier
                # Move constant Assignment
                if identifier in declarations:
                    node = declarations[identifier]
                    node.children[1] = child
                    child.parent = node
                    declarations.pop(identifier)
                self.children.remove(child)


    def processToken(self, token):
        if token == '#include <stdio.h>':
            self.useSTDIO = True

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        if self.useSTDIO:  # declare the imported IO functions
            file.write('declare i32 @printf(i8*, ...)\n')
            file.write('declare i32 @scanf(i8*, ...)\n')

        for child in self.children:
            child.toLLVM(file)


class CodeBodyNode(ASTNode):
    def __init__(self):
        super().__init__()
        self.counterTable = dict()

        self.hasReturn = False
        self.isVoidFunction = False
        self.pathsWithNoReturn = 0

    def startDFS(self):
        # build a new symbol table
        global symbolTables
        newSymbolTable = SymbolTableNode()
        symbolTables[-1].add(newSymbolTable)
        symbolTables.append(newSymbolTable)

        # Remove unused expressions
        # Find out if a codeBody always has a return. It has a return if a return exists in the codeBody, if each
        # path in the codeBody has a return or if a parent code block has a return
        # Remove unreachable code
        index = 0
        while index < len(self.children):
            child = self.children[index]
            if isinstance(child, OperationNode):
                child.printWarning("Unused expression: {}".format(child.text()))
                self.children.remove(child)
            if isinstance(child, ReturnStatementNode):
                self.hasReturn = True
                index = self.children.index(child)
                if index < len(self.children) - 1:
                    self.children[-1].printWarning("Unreachable Code")
                self.children = self.children[:index+1]
            if isinstance(child, IfStatementNode) or isinstance(child, WhileStatementNode):
                self.pathsWithNoReturn += 2
            if child in self.children:  # child is not removed => update index
                index += 1

        if not self.hasReturn:
            parent = self.parent
            while not isinstance(parent, CodeBodyNode) and not isinstance(parent, FunctionDefinitionNode):
                parent = parent.parent
            if isinstance(parent, CodeBodyNode):
                if parent.hasReturn:
                    self.hasReturn = True
                self.isVoidFunction = parent.isVoidFunction

    def endDFS(self):
        # symbol table is finished, pop from stack

        self.symbolTable = symbolTables.pop()

        if self.hasReturn:
            parent = self.parent
            while not isinstance(parent, CodeBodyNode) and not isinstance(parent, FunctionDefinitionNode):
                parent = parent.parent
            if isinstance(parent, CodeBodyNode):
                if not parent.hasReturn:
                    parent.pathsWithNoReturn -= 1
                    if parent.pathsWithNoReturn == 0:  # Each separate path has a return
                        parent.hasReturn = True
        if not self.hasReturn and not self.isVoidFunction:
            self.throwError("Control reaches end of non-void function")

    def canMerge(self, node):
        return False

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        if codeBody != None:
            self.counterTable = copy.deepcopy(codeBody.counterTable)
        func = isinstance(self.parent, FunctionDefinitionNode)
        # If a function body, add the arguments of the function
        if func:
            file.write("{\n")
            symbolTable = self.parent.symbolTable.symbolTable
            amountOfArguments = len(symbolTable)
            self.parent.counter += amountOfArguments
            for identifier, typename in symbolTable.items():
                typeAndAlign = llvm.checkTypeAndAlign(typename, True)
                localNumber = funcDef.getLocalNumber(typeAndAlign)
                # %4 = alloca i32, align 4
                file.write("%" + str(localNumber) + " = alloca " + str(typeAndAlign[0][0:-1]) + ", align " + str(
                    typeAndAlign[1]) + "\n")
                # store i32 %0, i32* %4, align 4
                file.write("store " + str(typeAndAlign[0][0:-1]) + " %" + str(localNumber - amountOfArguments - 1) + ", "
                           + str(typeAndAlign[0]) + " %" + str(localNumber) + ", align " + str(typeAndAlign[1]) + "\n")
                self.counterTable[identifier] = localNumber  # Link the var and localNumber with each other
        returned = False
        for child in self.children:
            child.toLLVM(file, funcDef, self)
            # Stop if we hit the return in the body
            if isinstance(child, ReturnStatementNode):
                returned = True
                break
        # If a function body and there wasn't a return statement, add one
        if func and not returned:
            if self.parent.children[0].children[0].typename == "void":
                file.write("ret void\n")
            elif self.parent.children[0].children[0].typename == "int":
                file.write("ret i32 0\n")
            elif self.parent.children[0].children[0].typename == "char":
                file.write("ret i8 0\n")
            elif self.parent.children[0].children[0].typename == "float":
                file.write("ret float 0x0000000000000000\n")
        if func:
            file.write("}\n")


class StatementNode(ASTNode):
    pass


class ReturnStatementNode(ASTNode):

    # Throws errors or prints warnings depending on the nominal return type and the effective return type
    def compatibleTypes(self, lhsType, rhsType):
        if lhsType == 'void' and rhsType != 'void':
            self.throwError("void function should not return a value")

        if lhsType != 'void' and rhsType == 'void':
            self.throwError("Non-void function should return a value")

        if lhsType in ['char', 'int'] and rhsType in ['int', 'float'] and lhsType != rhsType:
            self.printWarning("possible loss of information by returning type {} from a function returning type {}".
                              format(rhsType, lhsType))

        if (lhsType == 'float' or rhsType == 'float') and (lhsType.count('*') > 0 or rhsType.count('*') > 0
                                                           or rhsType.count('[') > 0):
            self.throwError('Returning {} from a function with incompatible result type {}"'.format(rhsType, lhsType))

        if lhsType.count('*') != rhsType.count('*') + rhsType.count('['):
            if lhsType.count('*') == 0:
                self.printWarning(
                    "Incompatible pointer to integer conversion returning {} from a function with return type {}".format(
                        rhsType, lhsType))
            elif lhsType.count('*') == 0:
                self.printWarning(
                    "Incompatible integer to pointer conversion returning {} from a function with return type {}".format(
                        lhsType, rhsType))
            else:
                self.printWarning(
                    "Incompatible pointer types returning {} from a function with return type {}".format(rhsType, lhsType))
        elif lhsType.count('*') > 0 and lhsType.split('*')[0] != rhsType.split('*')[0]:
            self.printWarning(
                "Incompatible pointer types returning {} from a function with return type {}".format(rhsType, lhsType))

    def endDFS(self):
        # check for compatible return types
        definition = self.parent
        while not isinstance(definition, FunctionDefinitionNode):
            definition = definition.parent

        returnType = definition.children[0].children[0].typename
        if len(self.children) == 0:
            type = 'void'
        else:
            type = self.children[0].type()
        self.compatibleTypes(returnType, type)

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        if len(self.children) == 0:
            file.write("ret void\n")
        else:
            llvmReturnType = llvm.checkTypeAndAlign(funcDef.children[0].children[0].typename)[0]
            file.write("ret " + str(llvmReturnType) + " " + str(
                self.children[0].toLLVM(file, funcDef, codeBody, llvmReturnType)) + "\n")
        # The return operation in llvm uses a register, so add 1 to the counter
        funcDef.getLocalNumber(llvm.checkTypeAndAlign('return'))


class DereferenceNode(ASTNode):
    def __init__(self):
        ASTNode.__init__(self)
        self.dereference = ''

    def processToken(self, token):
        self.dereference += token

    def text(self):
        return str(self.dereference)

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.dereference + '"];\n'

    def startDFS(self):
        # Check if the identifier that is dereferenced exists
        identifier = self.dereference.split('&')[-1]
        if not symbolTables[-1].exists(identifier) and not functionTable.exists(identifier):
            raise Exception(
                "Identifier " + identifier + " not found at " + str(self.line) + ":" + str(self.column))

    def type(self):
        identifier = self.dereference[1:]
        if len(symbolTables) != 0:  # while building the symbolTables
            if symbolTables[-1].exists(identifier):
                return symbolTables[-1].getEntry(identifier) + '*'
        else:
            parent = self.parent
            while parent.symbolTable is None:
                parent = parent.parent
            if parent.symbolTable.exists(identifier):
                return parent.symbolTable.getEntry(identifier) + '*'

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        temp = llvm.getLLVMOfCVarible(self.dereference[1:len(self.dereference)], funcDef, codeBody)
        varName = temp[0]
        typeAndAlign = temp[1]
        if returnType is None:
            return llvm.changeLLVMType(str(typeAndAlign[0]), varName, funcDef, file)
        else:
            return llvm.changeLLVMType(returnType, varName, funcDef, file)



class DepointerNode(ASTNode):
    def __init__(self):
        ASTNode.__init__(self)
        self.depointer = ''

    def processToken(self, token):
        self.depointer += token

    def text(self):
        return self.depointer

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.depointer + '"];\n'

    def type(self):
        identifier = self.depointer.split('*')[-1]
        type = symbolTables[-1].getEntry(identifier)
        type = type.split('*')[0] + (type.count('*') - self.depointer.count('*')) * '*'
        return type

    def startDFS(self):
        identifier = self.depointer.split('*')[-1]
        if not symbolTables[-1].exists(identifier) and not functionTable.exists(identifier):
            print(symbolTables[-1].symbolTable)
            raise Exception(
                "Identifier " + identifier + " not found at " + str(self.line) + ":" + str(self.column))
        type = symbolTables[-1].getEntry(identifier)
        if type.count('*') < self.depointer.count('*'):
            self.throwError("Indirection requires pointer operand ('{}' invalid)".format(type.split('*')[0]))

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        depointerAmount = 0
        for i in range(len(self.depointer)):
            if self.depointer[i] == '*':
                depointerAmount += 1
            if self.depointer[i] != '*':
                break
        var = llvm.getValueOfVariable(self.depointer[depointerAmount:len(self.depointer)], funcDef, codeBody, file)
        for _ in range(depointerAmount - 1):
            var = llvm.getValueOfVariable(var, funcDef, codeBody, file)
        # var = llvm.getValueOfVariable(var, funcDef, codeBody, file)

        if returnType != 'ASSIGN':
            var = llvm.getValueOfVariable(var, funcDef, codeBody, file)
        else:
            returnType = None

        if returnType is None:
            return var
        else:
            return llvm.changeLLVMType(returnType, var, funcDef, file)



class ElseStatementNode(ASTNode):
    def startDFS(self):
        if not isinstance(self.children[0], CodeBodyNode):  # If there is only one statement, put it into a codebody
            codeBody = CodeBodyNode()
            codeBody.add(self.children[0])
            self.children[0] = codeBody
            codeBody.parent = self

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        self.children[0].toLLVM(file, funcDef, codeBody)


class IfStatementNode(ASTNode):
    def startDFS(self):
        if not isinstance(self.children[1], CodeBodyNode):  # If there is only one statement, put it into a codebody
            codeBody = CodeBodyNode()
            codeBody.add(self.children[1])
            self.children[1] = codeBody
            codeBody.parent = self

    def endDFS(self):
        if isinstance(self.children[0], ValueNode):  # Constante in if-statement, dus we kunnen vereenvoudigen
            value = self.children[0].value
            index = self.parent.children.index(self)
            if value:  # If statement is always true
                self.parent.children[index] = self.children[1]
                self.parent.children[index].parent = self.parent
                self.children[0].printWarning("Condition is always true")
            else:  # If statement is always false
                self.children[0].printWarning("Condition is always false")
                if len(self.children) == 3:  # Else statement
                    self.parent.children[index] = self.children[2].children[0]
                    self.parent.children[index].parent = self.parent
                else:  # Geen else statement
                    self.parent.children.pop(index)



    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        ELSE = len(self.children) == 3
        resultLLVMVar = self.children[0].toLLVM(file, funcDef, codeBody)
        # If the llvm var isn't the result from comparison, we have to see if it's zero or not
        if not isinstance(self.children[0], ComparisonNode):
            resultLLVMVar = llvm.writeLLVMCompareWithZero(resultLLVMVar, funcDef, codeBody, file)

        global labelCounter
        labelCounter += 1
        label1 = 'if' + str(labelCounter)

        label2 = 'endif' + str(labelCounter)

        # Check if there's an else statement, if so also pre-write the codeBody of the else statement
        label3 = 'ERROR'
        if ELSE:
            label2 = 'else' + str(labelCounter)
            label3 = 'endif' + str(labelCounter)

        # br i1 %5, %something1, %something2
        file.write('br i1 ' + str(resultLLVMVar) + ', label %' + str(label1) + ', label %' + str(label2) + '\n\n')
        # something1:
        file.write(label1 + ':\n')
        # codeBody of the if statement
        self.children[1].toLLVM(file, funcDef, codeBody)
        if ELSE:
            # br label %something3
            file.write('br label %' + str(label3) + '\n\n')
        else:
            # br label %something2
            file.write('br label %' + str(label2) + '\n\n')
        # something2:
        file.write(label2 + ':\n')
        if ELSE:
            # codeBody of the else statement
            self.children[2].toLLVM(file, funcDef, codeBody)

            # br label %something3
            file.write('br label %' + str(label3) + '\n\n')
            # something3:
            file.write(label3 + ':\n')

    def toMIPS(self, file):

        for child in self.children:
            child.toMIPS(file)

class WhileStatementNode(ASTNode):
    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        global labelCounter
        labelCounter += 1
        label1 = 'while' + str(labelCounter)
        # br label %something1  (while check)
        file.write('br label %' + str(label1) + '\n\n')

        # something1:  (check statement)
        file.write(label1 + ':\n')
        resultLLVMVar = self.children[0].toLLVM(file, funcDef, codeBody)
        # If the llvm var isn't the result from comparison, we have to see if it's zero or not
        if not isinstance(self.children[0], ComparisonNode):
            resultLLVMVar = llvm.writeLLVMCompareWithZero(resultLLVMVar, funcDef, codeBody, file)

        label2 = 'inwhile' + str(labelCounter)

        label3 = 'endwhile' + str(labelCounter)

        # br i1 %3, label %something2, label %something3
        file.write('br i1 ' + str(resultLLVMVar) + ', label %' + str(label2) + ', label %' + str(label3) + '\n\n')

        # something2:  (while true)
        file.write(label2 + ':\n')
        self.children[1].toLLVM(file, funcDef, codeBody)
        # br label %something1  (while check)
        file.write('br label %' + str(label1) + '\n\n')

        # something3:  (stop while)
        file.write(label3 + ':\n')

    def endDFS(self):
        if isinstance(self.children[0], ValueNode):
            if self.children[0].value:  # always true
                self.printWarning("Endless loop")
            else: # always false
                self.printWarning("Condition is always False")



class TypeNameNode(ASTNode):

    def __init__(self):
        ASTNode.__init__(self)
        self.typename = ''

    def processToken(self, token):
        self.typename += token

    def text(self):
        return self.typename

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.typename + '"];\n'


class DeclarationNode(ASTNode):
    def startDFS(self):
        # Add entry to symbolTable
        typename = self.children[0].typename
        identifier = self.children[1].identifier
        if identifier in reservedWords:
            self.throwError("Invalid usage of reserved keyword {}  as identifier ".format(identifier))
        symbolTables[-1].addSymbol(typename, identifier)

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        typeAndAlign = llvm.checkTypeAndAlign(self.children[0].typename, True)
        localNumber = funcDef.getLocalNumber(typeAndAlign)
        identifier = self.children[1].identifier
        codeBody.counterTable[identifier] = localNumber  # Link the C var and localNumber with each other
        # %2 = alloca i32, align 4
        file.write('%' + str(localNumber) + ' = alloca ' + str(typeAndAlign[0][0:-1]) + ', align ' + str(
            typeAndAlign[1]) + "\n")
        if len(self.children) == 3:
            value = self.children[2].toLLVM(file, funcDef, codeBody, typeAndAlign[0][0:-1])
        else:
            if llvm.isPointer(typeAndAlign[0][0:-1]):
                value = 'null'
            elif typeAndAlign[0][0:-1] == 'float':
                value = '0x0000000000000000'
            else:
                value = '0'
        # store i32 %3, i32* %2, align 4
        file.write('store ' + str(typeAndAlign[0][0:-1]) + ' ' + str(value) + ', ' + str(
            typeAndAlign[0]) + ' %' + str(localNumber) + ', align ' + str(typeAndAlign[1]) + '\n')


class ArrayDeclarationNode(ASTNode):
    def __init__(self):
        ASTNode.__init__(self)

    def compatibleInitializerTypes(self, lhsType, rhsType):
        if lhsType in ['char', 'int'] and rhsType in ['int', 'float'] and lhsType != rhsType:
            self.printWarning("possible loss of information by assigning type {} to type {}".format(rhsType, lhsType))

        if (lhsType == 'float' or rhsType == 'float') and (lhsType.count('*') > 0 or rhsType.count('*') > 0
                                                           or rhsType.count('[') > 0):
            self.throwError('initializing {} with an expression of type {}"'.format(lhsType, rhsType))

        if lhsType.count('*') != rhsType.count('*') + rhsType.count('['):
            if lhsType.count('*') == 0:
                self.printWarning(
                    "Incompatible pointer to integer conversion initializing {} with an expression of type {}".format(
                        lhsType,
                        rhsType))
            elif lhsType.count('*') == 0:
                self.printWarning(
                    "Incompatible pointer to integer conversion initializing {} with an expression of type {}".format(
                        lhsType,
                        rhsType))
            else:
                self.printWarning(
                    "Incompatible pointer types initializing {} with an expression of type {}".format(lhsType, rhsType))
        elif lhsType.count('*') > 0 and lhsType.split('*')[0] != rhsType.split('*')[0]:
            self.printWarning(
                "Incompatible pointer types initializing {} with an expression of type {}".format(lhsType, rhsType))

    def startDFS(self):
        # Calculate the array size and add an entry in the SymbolTable
        typename = self.children[0].typename
        identifier = self.children[1].identifier
        size = ' '
        if len(self.children) == 4:
            size = self.children[2].value

        if len(self.children) == 3:
            if isinstance(self.children[2], ArrayListNode):
                size = len(self.children[2].children)
            elif isinstance(self.children[2], StringValueNode):
                size = len(self.children[2].value) + 1
            else:
                size = self.children[2].value
        typename = typename + '[' + str(size) + ']'

        if identifier in reservedWords:
            self.throwError("Invalid usage of reserved keyword {}  as identifier ".format(identifier))
        symbolTables[-1].addSymbol(typename, identifier)

    def endDFS(self):
        # Check if the initializing values are compatible with the array type
        typename = self.children[0].typename
        if len(self.children) == 4:
            for child in self.children[3].children:
                self.compatibleInitializerTypes(typename, child.type())

        if len(self.children) == 3:
            if isinstance(self.children[2], ArrayListNode):
                for child in self.children[2].children:
                    self.compatibleInitializerTypes(typename, child.type())

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        arrayList = None
        typename = '['
        identifier = self.children[1].identifier
        if isinstance(self.children[2], ArrayListNode):
            arrayList = self.children[2].children
            typename += str(len(self.children[2].children))
        else:
            typename += str(self.children[2].toLLVM(file, funcDef, codeBody, 'i32'))
            if len(self.children) == 4:
                arrayList = self.children[3].children
        typename += ' x ' + str(self.children[0].typename) + ']'

        typeAndAlign = llvm.checkTypeAndAlign(typename, True)
        localNumber = funcDef.getLocalNumber(typeAndAlign)
        codeBody.counterTable[identifier] = localNumber  # Link the C var and localNumber with each other
        # %1 = alloca [13 x i32], align 16
        file.write('%' + str(localNumber) + ' = alloca ' + str(typeAndAlign[0][:-1]) + ', align ' + typeAndAlign[1] + '\n')

        childType = llvm.getArrayTypeInfo(typeAndAlign[0])[1]
        # If the array is initialized, add the values
        if arrayList is not None:
            formerLocalNumber = 0
            for child in arrayList:
                typeAndAlign1 = llvm.checkTypeAndAlign(childType, True)
                localNumber1 = funcDef.getLocalNumber(typeAndAlign1)
                if child == arrayList[0]:  # Get the pointer
                    file.write("%{} = getelementptr inbounds {}, {} %{}, i64 0, i64 0\n"
                               .format(localNumber1, typeAndAlign[0][:-1], typeAndAlign[0], localNumber))
                else:  # Take the pointer of the next element
                    file.write("%{} = getelementptr inbounds {}, {} %{}, i64 1\n"
                               .format(localNumber1, childType, typeAndAlign1[0], formerLocalNumber))
                # Keep the last pointer in mind
                formerLocalNumber = localNumber1
                # Store the value in the pointer
                file.write("store {} {}, {}* %{}, align {}\n"
                           .format(childType, child.toLLVM(file, funcDef, codeBody, childType),
                                   childType, localNumber1, typeAndAlign1[1]))
        length = llvm.getArrayTypeInfo(typeAndAlign[0])[0]
        if arrayList == None or len(arrayList) < length:
            if llvm.isPointer(childType):
                value = 'null'
            elif childType == 'float':
                value = '0x0000000000000000'
            else:
                value = '0'
            if arrayList == None:
                arrayListLen = 0
            else:
                arrayListLen = len(arrayList)
            for i in range(arrayListLen, length):
                typeAndAlign1 = llvm.checkTypeAndAlign(childType, True)
                localNumber1 = funcDef.getLocalNumber(typeAndAlign1)
                if i == 0:
                    file.write("%{} = getelementptr inbounds {}, {} %{}, i64 0, i64 0\n"
                               .format(localNumber1, typeAndAlign[0][:-1], typeAndAlign[0], localNumber))
                else:
                    file.write("%{} = getelementptr inbounds {}, {} %{}, i64 1\n"
                               .format(localNumber1, childType, typeAndAlign1[0], formerLocalNumber))
                file.write("store {} {}, {}* %{}, align {}\n"
                           .format(childType, value,
                                   childType, localNumber1, typeAndAlign1[1]))
                formerLocalNumber = localNumber1


class ConstantDeclarationNode(DeclarationNode):
    def startDFS(self):
        # Add an entry in the symbol Table
        typename = self.children[0].typename
        if isinstance(self.children[1], IdentifierNode):
            identifier = self.children[1].identifier
        else:
            identifier = self.children[1].children[0].identifier
        if identifier in reservedWords:
            self.throwError('Invalid usage of reserved keyword {}  as identifier '.format(identifier))
        symbolTables[-1].addSymbol(typename, identifier)

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        typeAndAlign = llvm.checkTypeAndAlign(self.children[0].typename, True)
        valueType = typeAndAlign[0][0:-1]  # C var is a pointer for a value, so the values type is
        if isinstance(self.parent, ProgramNode):
            if isinstance(self.children[1], IdentifierNode):
                if llvm.isPointer(valueType):
                    standardValue = 'null'
                elif valueType == 'float':
                    standardValue = '0x0000000000000000'
                else:
                    standardValue = '0'
                # @a = common global i32 0, align 4
                identifier = self.children[1].identifier
                file.write(
                    '@' + str(identifier) + ' = common global ' + str(valueType) + ' ' + str(standardValue) + ', align ' +
                    typeAndAlign[1] + '\n')

            else:  # If value is given
                identifier = self.children[1].children[0].identifier
                # Create temporary variables
                tempFuncDef = FunctionDefinitionNode()
                tempFuncDef.parent = self.parent
                tempCodeBody = CodeBodyNode()
                tempFile = llvm.FileLookALike()
                # Execute the toLLVM function of the value constantAssignment
                endVar = self.children[1].children[1].toLLVM(tempFile, tempFuncDef, tempCodeBody, valueType)
                # Put the outputted llvm commands by the toLLVM function on one line
                endStr = tempFile.putOnOneLine(endVar, tempFuncDef, tempCodeBody)
                # @a = global i32 5, align 4 or @d11 = global i8* bitcast (i32* getelementptr (i32, i32* @b, i64 32) to i8*), align 8
                file.write('@' + str(identifier) + ' = global ' + str(valueType) + ' ' + str(endStr) + ', align ' + typeAndAlign[1] + '\n')

            self.parent.typeAndAlignTable[identifier] = typeAndAlign

        elif isinstance(self.parent, CodeBodyNode):
            # %1 = alloca i32, align 4
            localNumber = funcDef.getLocalNumber(typeAndAlign)
            file.write('%' + str(localNumber) + ' = alloca ' + str(valueType) + ', align ' + str(
                typeAndAlign[1]) + '\n')
            if isinstance(self.children[1], IdentifierNode):
                identifier = self.children[1].identifier
                if llvm.isPointer(valueType):
                    value = 'null'
                elif valueType == 'float':
                    value = '0x0000000000000000'
                else:
                    value = '0'
            else:
                identifier = self.children[1].children[0].identifier
                value = self.children[1].children[1].toLLVM(file, funcDef, codeBody, valueType)
                # store i32 3, i32* %1, align 4
            file.write('store ' + str(valueType) + ' ' + str(value) + ', ' + str(
                typeAndAlign[0]) + ' %' + str(localNumber) + ', align ' + str(typeAndAlign[1]) + '\n')
            codeBody.counterTable[identifier] = localNumber  # Link the C var and localNumber with each other


class ConstantArrayDeclarationNode(ArrayDeclarationNode):
    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        if isinstance(self.parent, CodeBodyNode):
            return super().toLLVM(file, funcDef, codeBody, returnType)
        elif isinstance(self.parent, ProgramNode):
            arrayList = None
            typename = '['
            identifier = self.children[1].identifier
            if isinstance(self.children[2], ConstantArrayListNode):
                arrayList = self.children[2].children
                typename += str(len(self.children[2].children))
            else:
                typename += str(self.children[2].value)
                if len(self.children) == 4:
                    arrayList = self.children[3].children
            typename += ' x ' + str(self.children[0].typename) + ']'
            typeAndAlign = llvm.checkTypeAndAlign(typename, True)
            self.parent.typeAndAlignTable[identifier] = typeAndAlign
            childType = llvm.getArrayTypeInfo(typeAndAlign[0])[1]
            file.write("@{} = global {} [".format(identifier, typeAndAlign[0][:-1]))
            if arrayList is not None:
                for child in arrayList:
                    file.write("{} {}".format(childType, child.toLLVM(file, funcDef, codeBody, childType)))
                    if child != arrayList[-1]:
                        file.write(', ')
            length = llvm.getArrayTypeInfo(typeAndAlign[0])[0]
            if arrayList == None or len(arrayList) < length:
                if llvm.isPointer(childType):
                    value = 'null'
                elif childType == 'float':
                    value = '0x0000000000000000'
                else:
                    value = '0'
                if arrayList == None:
                    arrayListLen = 0
                else:
                    arrayListLen = len(arrayList)
                    file.write(', ')
                for i in range(arrayListLen, length):
                    file.write("{} {}".format(childType, value))
                    if i != length - 1:
                        file.write(', ')
            file.write('], align {}\n'.format(typeAndAlign[1]))




class ConstantValueNode(ASTNode):
    pass


class ConstantNode(ASTNode):
    pass


class ArrayListNode(ASTNode):
    pass


class ConstantArrayListNode(ArrayListNode):
    pass


class FunctionDeclarationNode(ASTNode):
    def startDFS(self):
        # Create a function table entry and do some rudimentary checks

        typename = self.children[0].typename
        identifier = self.children[1].identifier

        arguments = list()

        if len(self.children) > 2:
            for i in range(0, len(self.children[2].children)):
                if isinstance(self.children[2].children[i], ArrayTypeNode):  # Werkt alleen voor one dimensional arrays
                    argumentType = self.children[2].children[i].children[0].typename + '*'
                    arguments.append(argumentType)
                    if i == len(self.children)-1 or not isinstance(self.children[2].children[i+1], IdentifierNode) and \
                            isinstance(self.parent, FunctionDefinitionNode):
                        self.children[2].children[i].throwError("Parameter name omitted")

                elif isinstance(self.children[2].children[i], TypeNameNode):
                    argumentType = self.children[2].children[i].typename
                    arguments.append(argumentType)

        if functionTable.exists(identifier) and not functionTable.signatureExists(typename, identifier, arguments):
            self.throwError("function {} is redeclared with a different signature".format(identifier))

        functionTable.addFunction(typename, identifier, arguments, isinstance(self.parent, FunctionDefinitionNode))

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        typeAndAlign = llvm.checkTypeAndAlign(self.children[0].typename)
        declaration = False
        # file.write("\n")
        if isinstance(self.parent, FunctionDefinitionNode):
            file.write("\ndefine ")
        else:
            return
            # declaration = True
            # file.write("declare ")
        if typeAndAlign[0] == "i8":
            file.write("signext ")
        file.write(str(typeAndAlign[0]) + " @" + str(self.children[1].identifier + "("))
        if len(self.children) == 2:
            # define i32 @main()
            file.write(")")
        elif len(self.children) == 3:
            # define void @f1(i32)
            for i in range(len(self.children[2].children)):
                if isinstance(self.children[2].children[i], IdentifierNode):
                    continue
                typeAndAlign = llvm.checkTypeAndAlign(self.children[2].children[i].typename)
                if i != 0:
                    file.write(", ")
                file.write(str(typeAndAlign[0]))
                if typeAndAlign[0] == "i8":
                    file.write(" signext")
            file.write(") ")
        if declaration:
            file.write("\n")


class ArgumentDeclarationListNode(ASTNode):
    pass


class FunctionDefinitionNode(ASTNode):
    def __init__(self):
        super().__init__()
        self.counter = 1
        self.typeAndAlignTable = dict()

    def getLocalNumber(self, typeAndAlign):
        self.typeAndAlignTable[str(self.counter)] = typeAndAlign  # Link the var and type for further use
        self.counter += 1
        return self.counter - 1

    def startDFS(self):
        # build a new symbol table

        identifier = self.children[0].children[1].identifier

        if functionTable.isDefined(identifier):
            self.throwError("Redefinition of function {}".format(identifier))
        global symbolTables
        newSymbolTable = SymbolTableNode()
        symbolTables[-1].add(newSymbolTable)
        symbolTables.append(newSymbolTable)

        if self.children[0].children[0].typename == 'void':
            self.children[1].isVoidFunction = True

        if len(self.children[0].children) < 3:  # geen argumenten, dus skip
            return
        arguments = self.children[0].children[2]

        for i in range(0, len(arguments.children)):
            typename = None
            identifier = None
            if isinstance(arguments.children[i], ArrayTypeNode):  # Werkt alleen voor one dimensional arrays
                typename = arguments.children[i].children[0].typename + '*'
                identifier = arguments.children[i].children[1].identifier
            elif isinstance(arguments.children[i], TypeNameNode):
                typename = arguments.children[i].typename
                identifier = arguments.children[i + 1].identifier

            if typename is None:
                continue

            if identifier in reservedWords:
                arguments.throwError("Invalid usage of reserved keyword {}  as identifier ".format(identifier))
            symbolTables[-1].addSymbol(typename, identifier)

    def endDFS(self):
        # symbol table is finished, pop from stack
        self.symbolTable = symbolTables.pop()

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        # LLVM output part 1 here
        for child in self.children:
            child.toLLVM(file, self)
        # LLVM output part 2 here


class ReturnTypeNode(TypeNameNode):
    pass


class ArrayElementNode(ASTNode):
    def type(self):
        identifier = self.children[0].identifier
        type = symbolTables[-1].getEntry(identifier)
        return type.split('[')[0]  # simplistic approach, only works for one dimensional arrays

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        temp = llvm.getLLVMOfCVarible(self.children[0].identifier, funcDef, codeBody)
        varName = temp[0]
        typeAndAlign = temp[1]
        llvmReturnType = llvm.getArrayTypeInfo(typeAndAlign[0])[1] + '*'
        localNumber = funcDef.getLocalNumber(llvm.checkTypeAndAlign(llvmReturnType))
        # %2 = getelementptr inbounds [13 x i32], [13 x i32]* %1, i64 0, i64 1
        file.write('%' + str(localNumber) + ' = getelementptr inbounds ' + str(typeAndAlign[0][0:-1]) + ', ' + str(typeAndAlign[0]) + ' ' + str(varName) + ', i64 0, i64 ' + str(self.children[1].value) + '\n')
        varName = '%' + str(localNumber)

        if returnType != 'ASSIGN':
            varName = llvm.getValueOfVariable(varName, funcDef, codeBody, file)
        else:
            returnType = None

        if returnType is None:
            return varName
        else:
            return llvm.changeLLVMType(returnType, varName, funcDef, file)


class AssignmentNode(ASTNode):
    def type(self):
        return self.children[0].type()

    def startDFS(self):
        # TODO: check this for array elements assigning to self as well
        if not isinstance(self.children[0], ArrayElementNode) and not isinstance(self.children[0], DepointerNode):
            identifier = self.children[0].identifier
            if isinstance(self.children[1], IdentifierNode):  # Assign identifier to same identifier
                if identifier == self.children[1].identifier:
                    self.parent.children.remove(self)
                    self.printWarning("Explicitly Assigning variable to itself")

    def endDFS(self):
        # Give warnings or errors for type conversion / invalid types for operations

        lhsType = self.children[0].type()
        rhsType = self.children[1].type()

        if lhsType in ['char', 'int'] and rhsType in ['int', 'float'] and lhsType != rhsType:
            self.printWarning("possible loss of information by assigning type {} to type {}".format(rhsType, lhsType))

        if '[' in lhsType:
            self.throwError("Array type {} is non-assignable".format(lhsType))

        if (lhsType == 'float' or rhsType == 'float') and (lhsType.count('*') > 0 or rhsType.count('*') > 0
                                                           or rhsType.count('[') > 0):
            self.throwError('Assigning to {} from incompatible type {}'.format(lhsType, rhsType))

        if lhsType.count('*') != rhsType.count('*') + rhsType.count('['):
            if lhsType.count('*') == 0:
                self.printWarning(
                    "Incompatible pointer to integer conversion assigning to {} from {}".format(lhsType, rhsType))
            elif lhsType.count('*') == 0:
                self.printWarning(
                    "Incompatible integer to pointer conversion assigning to {} from {}".format(lhsType, rhsType))
            else:
                self.printWarning("Incompatible pointer types assigning to {} from {}".format(lhsType, rhsType))
        elif lhsType.count('*') > 0 and lhsType.split('*')[0] != rhsType.split('*')[0]:
            self.printWarning("Incompatible pointer types assigning to {} from {}".format(lhsType, rhsType))

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        if isinstance(self.children[0], ArrayElementNode):
            var = llvm.writeLLVMStoreForCVariable(self.children[0].toLLVM(file, funcDef, codeBody, 'ASSIGN'), self.children[1].toLLVM(file, funcDef, codeBody), funcDef, codeBody, file)
        elif isinstance(self.children[0], DepointerNode):
            var = llvm.writeLLVMStoreForCVariable(self.children[0].toLLVM(file, funcDef, codeBody, 'ASSIGN'), self.children[1].toLLVM(file, funcDef, codeBody), funcDef, codeBody, file)
        else:
            var = llvm.writeLLVMStoreForCVariable(self.children[0].identifier, self.children[1].toLLVM(file, funcDef, codeBody), funcDef, codeBody, file)
        if returnType is not None:
            return llvm.changeLLVMType(returnType, llvm.getValueOfVariable(var, funcDef, codeBody, file), funcDef, file)


class ConstantAssignmentNode(AssignmentNode):
    pass


class ValueNode(ASTNode):
    def __init__(self):
        ASTNode.__init__(self)
        self.value = None

    def text(self):
        return ''

    def type(self):
        return ''

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.text() + '"];\n'

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        if returnType == None:
            return llvm.valueTransformer(self.type(), self.value)
        else:
            return llvm.valueTransformer(returnType, self.value)


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

    def text(self):
        return ('-' if self.sign < 0 else '') + str(self.value)

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.text() + '"];\n'

    def type(self):
        return 'int'


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
            self.fraction = token
            self.value = float(str(self.integer) + '.' + str(self.fraction))

    def text(self):
        return ('-' if self.sign < 0 else '') + str(self.value)

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.text() + '"];\n'

    def type(self):
        return 'float'


class CharValueNode(ValueNode):

    def processToken(self, token):
        self.value = token[1]

    def text(self):
        return 'char: {}'.format(ord(self.value))

    def type(self):
        return 'char'

class StringValueNode(ValueNode):
    def processToken(self, token):
        self.value = token[1:-1]

    def text(self):
        return '"' + self.value + '"'

    def type(self):
        return "cstring"

    def startDFS(self):
        # Replace by an array of chars

        replacement = ConstantArrayListNode()
        replacement.parent = self.parent
        index = self.parent.children.index(self)
        self.parent.children[index] = replacement
        i = 0
        while i < len(self.value):
            c = self.value[i]
            node = CharValueNode()
            if c == '\\' and i < len(self.value) - 1:
                c += self.value[i+1]
                i += 1
                if c == '\\n':
                    c = '\n'
                elif c == '\\\\':
                    c = '\\'
                else:
                    i += 1
                    continue
            node.value = c
            replacement.add(node)
            i += 1
        node = CharValueNode()
        node.value = chr(0)
        replacement.add(node)
        replacement.startDFS()


class FunctionCallNode(ASTNode):

    # Print warnings / throw errors if the given argument type doesn't match the expected type
    def compatibleArgumentTypes(self, lhsType, rhsType):
        if lhsType in ['char', 'int'] and rhsType in ['int', 'float'] and lhsType != rhsType:
            self.printWarning("possible loss of information by assigning type {} to type {}".format(rhsType, lhsType))

        if (lhsType == 'float' or rhsType == 'float') and (lhsType.count('*') > 0 or rhsType.count('*') > 0
                                                           or rhsType.count('[') > 0):
            self.throwError('Passing {} to parameter of incompatible type {}'.format(rhsType, lhsType))

        if lhsType.count('*') != rhsType.count('*') + rhsType.count('['):
            if lhsType.count('*') == 0:
                self.printWarning(
                    "Incompatible pointer to integer conversion passing {} to parameter of type {}".format(rhsType,
                                                                                                           lhsType))
            elif lhsType.count('*') == 0:
                self.printWarning(
                    "Incompatible pointer to integer conversion passing {} to parameter of type {}".format(rhsType,
                                                                                                           lhsType))
            else:
                self.printWarning(
                    "Incompatible pointer types passing {} to parameter of type {}".format(rhsType, lhsType))
        elif lhsType.count('*') > 0 and lhsType.split('*')[0] != rhsType.split('*')[0] and lhsType.split('*')[0] != rhsType.split('[')[0]:
            self.printWarning("Incompatible pointer types passing {} to parameter of type {}".format(rhsType, lhsType))

    def startDFS(self):
        # Do some rudimentary checks for the function Call
        identifier = self.children[0].identifier

        # check if function exists
        if not functionTable.exists(identifier):
            self.throwError("Identifier {} not found".format(identifier))

        # check if function is defined
        if not functionTable.isDefined(identifier):
            self.throwError("Function {} is not defined".format(identifier))

        argumentCount = 0
        if len(self.children) != 1:
            argumentCount = len(self.children[1].children)
        arguments = functionTable.functionTable[identifier][1]

        if len(arguments) != 0 and arguments[-1] == '...':
            # infinite arguments possible
            if argumentCount < len(arguments) - 1:
                self.throwError("Expected at least {} arguments, got()".format(len(arguments) - 1, argumentCount))
        else:
            if argumentCount != len(arguments):
                self.throwError("Expected {} arguments, got {}".format(len(arguments), argumentCount))


    def endDFS(self):
        # Type check each argument

        identifier = self.children[0].identifier
        arguments = functionTable.functionTable[identifier][1]
        if len(arguments) != 0 and arguments[-1] == '...':
            # infinite arguments possible
            for i in range(len(arguments) - 1):  # Don't check the optional arguments
                self.compatibleArgumentTypes(arguments[i], self.children[1].children[i].type())

        else:
            for i in range(len(arguments)):
                self.compatibleArgumentTypes(arguments[i], self.children[1].children[i].type())


    def type(self):
        if functionTable.exists(self.children[0].identifier):
            return functionTable.functionTable[self.children[0].identifier][0]

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        functionReturnType = returnType
        temp = funcDef.parent.functionTable.functionTable[self.children[0].identifier]
        returnType = temp [0]
        argumentTypes = temp[1]
        arguments = []

        argumentCount = 0
        if len(self.children) > 1:
            argumentCount = len(self.children[1].children)

        for i in range(argumentCount):
            child = self.children[1].children[i]
            loc = child.toLLVM(file, funcDef, codeBody)

            if i < len(argumentTypes) and argumentTypes[i] != '...':
                arguments.append(llvm.changeLLVMType(llvm.checkTypeAndAlign(argumentTypes[i])[0], loc, funcDef, file))
            else:
                arguments.append(loc)
                if self.children[0].identifier == 'printf' or self.children[0].identifier == 'scanf':  # printf doesn't like floats, it wants doubles
                    if child.type() == 'float':
                        # TODO: hacky code, refactor some time?

                        number = funcDef.getLocalNumber(('i64', '8'))
                        file.write('%{} = fpext float {} to double\n'.format(number, arguments[-1]))
                        arguments[-1] = '%' + str(number)

        localNumber = 'ERROR'
        typeAndAlign = llvm.checkTypeAndAlign(returnType)
        if returnType != 'void':
            localNumber = funcDef.getLocalNumber(typeAndAlign)
            # %8 = call signext i8 @f1(i32 %5, i8 signext %7)
            file.write('%' + str(localNumber) + ' = ')
        file.write('call ')
        if typeAndAlign[0] == 'i8':
            file.write('signext ')
        file.write(str(typeAndAlign[0]))
        if len(argumentTypes) > 0 and argumentTypes[-1] == '...':
            file.write(' (i8*, ...)')
        file.write(' @' + str(self.children[0].identifier + '('))
        if len(arguments) == 0:
            # call void @f2()
            file.write(')\n')
        else:
            # call void @f2(i32 %2, i32 %3)
            for i in range(len(self.children[1].children)):
                # child = self.children[1].children[i]
                typeAndAlign = llvm.checkTypeAndAlign(llvm.getLLVMTypeOfVariable(arguments[i], funcDef, codeBody))
                if typeAndAlign[0] == 'float' and (self.children[0].identifier == 'printf' or self.children[0].identifier == 'scanf'):
                    #TODO: more hacky code for printf shenanigans
                    typeAndAlign = ('i64', typeAndAlign[1])
                if i != 0:
                    file.write(', ')
                if llvm.getArrayTypeInfo(typeAndAlign[0]):  # convert array to pointer
                    type = (llvm.convertArrayToPointer(llvm.getArrayTypeInfo(typeAndAlign[0])))
                    file.write(type)
                else:
                    file.write(typeAndAlign[0])
                if typeAndAlign[0] == 'i8':
                    file.write(' signext')
                file.write(' ' + str(arguments[i]))
            file.write(")\n")
        if returnType != 'void':
            if functionReturnType is None:
                return '%' + str(localNumber)
            else:
                return llvm.changeLLVMType(functionReturnType, '%' + str(localNumber), funcDef, file)
        else:
            return ''


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

    def text(self):
        text = ''
        for child in self.children:
            text += child.text()
            if child != self.children[-1]:
                text += self.operator
        return text

    def canMerge(self, node):
        return ASTNode.canMerge(self, node) and node.operator == self.operator

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.operator + '"];\n'

    def isCompatibleType(self, type1, type2):
        # Should never be accessed by program
        self.throwError('Invalid types for binary operator {} : {}, {}'.format(self.operator, type1, type2))

    def mergeType(self, type1, type2):
        raise Exception("Not implemented for class {}".format(self.__class__))

    def mergeOperands(self, operands, specialCase=False):
        # Special case is for divisions of the type ((.../val1)/val2)/...
        # This needs to be folded to (.../(val1*val2))/...
        # Divisions of the type (val1/val2)/.. can still be folded the same way as all other operations


        type = operands[0].type()
        value = None
        for node in operands:
            self.isCompatibleType(type, node.type())
            type = self.mergeType(type, node.type())
            if value is None:
                if isinstance(node, CharValueNode):
                    value = ord(node.value)
                else:
                    value = node.value
            else:
                if specialCase and self.operator == '/':
                    if isinstance(node, CharValueNode):
                        value = eval("{}*{}".format(value, ord(node.value)))
                    else:
                        value = eval("{}*{}".format(value, node.value))
                else:
                    if isinstance(node, CharValueNode):
                        value = eval("{}{}{}".format(value, self.operator, ord(node.value)))
                    else:
                        value = eval("{}{}{}".format(value, self.operator, node.value))

        if type == 'float':
            node = FloatValueNode()
            node.value = float(value)
            return node
        if type == 'int':
            node = IntValueNode()
            node.value = int(value)
            return node
        if type == 'char':
            node = CharValueNode()
            node.value = chr(int(value) % 256)
            return node

    def foldExpression(self):
        newChildren = []
        temp = []
        for i in range(len(self.children)):
            if isinstance(self.children[i], ValueNode):
                temp.append(self.children[i])
            else:
                # Continuous constants (temp) can be folded in one constant
                if len(temp) < 2:  # Don't bother
                    for node in temp:
                        newChildren.append(node)
                    temp = []
                    newChildren.append(self.children[i])
                    continue
                newChildren.append(self.mergeOperands(temp, temp[0] != self.children[0]))
                newChildren.append(self.children[i])
                temp = []
        if len(temp) > 0:
            newChildren.append(self.mergeOperands(temp, temp[0] != self.children[0]))
        self.children.clear()
        if len(newChildren) == 1:
            # operation consists of only 1 child, push the child up
            index = self.parent.children.index(self)
            self.parent.children[index] = newChildren[0]
            self.parent.children[index].parent = self.parent
        else:
            for node in newChildren:
                self.add(node)


    def endDFS(self):
        self.foldExpression()

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        # operands = list()
        # for child in self.children:
        #     operands.append(child.toLLVM(file, funcDef, codeBody))
        if returnType is None:
            return llvm.writeLLVMOperation(self.operator, self.children, funcDef, codeBody, file)
        else:
            return llvm.changeLLVMType(returnType,
                                       llvm.writeLLVMOperation(self.operator, self.children, funcDef, codeBody, file),
                                       funcDef, file)


class SumNode(OperationNode):
    # Check if the lhs Type and the rhs type are compatible in a sum
    def isCompatibleType(self, type1, type2):
        if type1 in ['int', 'float', 'char'] and type2 in ['int', 'float', 'char']:
            return True
        if self.operator == '+' and (type1 in ['int', 'char'] and type2[-1] == '*'
                                     or type1[-1] == '*' and type2 in ['int', 'char']):
            return True
        if self.operator == '-' and type1[-1] == '*' and (type2 in ['int', 'char'] or type1 == type2):
            return True
        if self.operator == '-' and type1[-1] == '*' and type2[-1] == '*':
            self.throwError('{} and {} are not pointers to compatible types'.format(type1, type2))
        self.throwError('Invalid types for binary operator {} : {}, {}'.format(self.operator, type1, type2))

    # Find the correct type for a sum of two types
    def mergeType(self, type1, type2):
        if type1 == type2:
            return type1
        if type1 in ['char', 'int'] and type2 in ['int', 'float']:
            return type2
        if type1 in ['int', 'float'] and type2 in ['char', 'int']:
            return type1
        if type1[-1] == '*':
            return type1
        if type2[-1] == '*':
            return type2

    def type(self):
        type = None
        for child in self.children:
            if type is None:
                type = child.type()
            else:
                if self.isCompatibleType(type, child.type()):
                    type = self.mergeType(type, child.type())
        return type

    def foldExpression(self):
        OperationNode.foldExpression(self)
        if len(self.children) == 0:  # alles is al gefold door de normale foldExpression
            return
        temp = []
        for child in self.children:
            if isinstance(child, ValueNode):
                temp.append(child)

        if len(temp) == 0:  # niets kan gefold worden
            return

        result = self.mergeOperands(temp)
        result.parent = self
        if temp[0] == self.children[0]:
            # Result moet eerst in de children
            self.children[0] = result
        else:
            # Result moet laatst in de children
            self.children.append(result)

        for child in self.children:
            if isinstance(child, ValueNode) and child in temp:
                self.children.remove(child)


class ProductNode(OperationNode):
    def isCompatibleType(self, type1, type2):
        if type1 in ['int', 'float', 'char'] and type2 in ['int', 'float', 'char']:
            return True
        self.throwError('Invalid types for binary operator {} : {}, {}'.format(self.operator, type1, type2))

    def mergeType(self, type1, type2):
        if type1 == type2:
            return type1
        if type1 in ['char', 'int'] and type2 in ['int', 'float']:
            return type2
        if type1 in ['int', 'float'] and type2 in ['char', 'int']:
            return type1

    def type(self):
        type = None
        for child in self.children:
            if type is None:
                type = child.type()
            else:
                if self.isCompatibleType(type, child.type()):
                    type = self.mergeType(type, child.type())
        return type

    def foldExpression(self):
        OperationNode.foldExpression(self)
        if len(self.children) == 0:  # alles is al gefold door de normale foldExpression
            return
        temp = []
        for child in self.children:
            if isinstance(child, ValueNode):
                temp.append(child)

        if len(temp) == 0:  # niets kan gefold worden
            return

        result = self.mergeOperands(temp)
        result.parent = self
        if len(temp) != 0 and temp[0] == self.children[0]:
            # Result moet eerst in de children
            self.children[0] = result
        else:
            # Result moet laatst in de children
            self.children.append(result)

        for child in self.children:
            if isinstance(child, ValueNode) and child in temp:
                self.children.remove(child)


class ComparisonNode(OperationNode):

    # Prints a warning / throws an error if there are incompatible types in the comparison
    def isCompatibleType(self, type1, type2):
        if type1[-1] == '*' and type2[-1] == '*' and type1 != type2:
            self.printWarning('Comparison of distinct pointer types : {} , {}'.format(type1, type2))

        if (type1[-1] == '*' and type2[-1] != '*') or (type2[-1] == '*' and type1[-1] != '*'):
            self.printWarning('Comparison between pointer and integer : {} , {}'.format(type1, type2))

        return True

    def mergeType(self, type1, type2):
        if type1 == type2:
            return type1
        if type1 in ['char', 'int'] and type2 in ['int', 'float']:
            return type2
        if type1 in ['int', 'float'] and type2 in ['char', 'int']:
            return type1
        return 'int'

    def type(self):
        type = None
        for child in self.children:
            if type is None:
                type = child.type()
            else:
                if self.isCompatibleType(type, child.type()):
                    type = self.mergeType(type, child.type())
        return type


class OperatorAssignmentNode(ASTNode):
    def __init__(self):
        ASTNode.__init__(self)
        self.operator = None

    def processToken(self, token):
        if token != '=':
            self.operator = token

    def alias(self):
        index = self.parent.children.index(self)
        assignment = AssignmentNode()
        assignment.parent = self.parent
        self.parent.children[index] = assignment
        assignment.add(self.children[0])

        operation = None
        if self.operator == '+' or self.operator == '-':
            operation = SumNode()
        elif self.operator == '*' or self.operator == '/':
            operation = ProductNode()

        operation.operator = self.operator

        lhs = copy.deepcopy(self.children[0])
        lhs.id = lhs.count
        lhs.count += 1
        operation.add(lhs)
        operation.add(self.children[1])

        assignment.add(operation)

        return assignment

    def startDFS(self):
        alias = self.alias()
        alias.buildSymbolTable()


class ConstantComparisonNode(ComparisonNode):
    pass


class ConstantSumNode(SumNode):
    pass


class ConstantProductNode(ProductNode):
    pass


class ArrayTypeNode(ASTNode):
    pass

class IdentifierNode(ASTNode):

    def __init__(self):
        ASTNode.__init__(self)
        self.identifier = ''

    def processToken(self, token):
        self.identifier = token

    def text(self):
        return self.identifier

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.identifier + '"];\n'

    def startDFS(self):
        if not symbolTables[-1].exists(self.identifier) and not functionTable.exists(self.identifier):
            print(symbolTables[-1].symbolTable)
            raise Exception(
                "Identifier " + self.identifier + " not found at " + str(self.line) + ":" + str(self.column))

    def type(self):
        if len(symbolTables) != 0:  # while building the symbolTables
            if symbolTables[-1].exists(self.identifier):
                return symbolTables[-1].getEntry(self.identifier)
        else:
            parent = self.parent
            while parent.symbolTable is None:
                parent = parent.parent
            if parent.symbolTable.exists(self.identifier):
                return parent.symbolTable.getEntry(self.identifier)

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        if returnType is None:
            return llvm.getValueOfVariable(self.identifier, funcDef, codeBody, file)
        else:
            return llvm.changeLLVMType(returnType, llvm.getValueOfVariable(self.identifier, funcDef, codeBody, file), funcDef, file)