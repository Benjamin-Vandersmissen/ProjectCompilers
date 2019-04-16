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
    # expects fundDef to be a FuntionDefenitionNode. Only children of such a node need this argument!!
    # expects codeBody to be a CodeBodyNode. Only children of such a node need this argument!
    # expects returnType to be an llvm typename. Only nodes that return a value or variable can use this arhument!
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
        # TODO: add standaard shit in symboltable

    def endDFS(self):
        global symbolTables, functionTable
        self.symbolTable = symbolTables.pop()
        self.functionTable = functionTable

        # Optimise global assignments and declarations

        declarations = dict()
        for child in self.children:
            if isinstance(child, ConstantDeclarationNode):
                if isinstance(child.children[1], IdentifierNode):
                    declarations[child.children[1].identifier] = child
                else:
                    declarations[child.children[1].children[0].identifier] = child

        for child in reversed(self.children):
            if isinstance(child, ConstantAssignmentNode):
                identifier = child.children[0].identifier
                if identifier in declarations:
                    node = declarations[identifier]
                    node.children[1] = child
                    child.parent = node
                    declarations.pop(identifier)
                self.children.remove(child)


    def processToken(self, token):
        if token == '#include <stdio.h>':
            self.useSTDIO = True


class CodeBodyNode(ASTNode):
    def __init__(self):
        super().__init__()
        self.counterTable = dict()

    def startDFS(self):
        # build a new symbol table
        global symbolTables
        newSymbolTable = SymbolTableNode()
        symbolTables[-1].add(newSymbolTable)
        symbolTables.append(newSymbolTable)

        # Remove unused expressions
        for child in self.children:
            if isinstance(child, OperationNode):
                child.printWarning("Unused expression: {}".format(child.text()))
                self.children.remove(child)

    def canMerge(self, node):
        return False

    def endDFS(self):
        # symbol table is finished, pop from stack
        self.symbolTable = symbolTables.pop()

    # int a = 1 + 'A' + 2.01;
    # int main() {
    #     a = b;
    #     char a;
    #     a = b;
    #     {
    #         float a;
    #         a = b;
    #     }
    #     a = 1;
    # }

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        if codeBody != None:  # TODO: llvm: TEST (staat hierboven) als Benjamin ervoor gezorgt heeft dat een codeBody kind van een codeBody een codeBody blijft en niet gemerged wordt
            self.counterTable = copy.deepcopy(codeBody.counterTable)
        func = isinstance(self.parent, FunctionDefinitionNode)
        # If a function body, add the arguments of the function
        if func:
            file.write("{\n")
            symbolTable = self.parent.symbolTable.symbolTable
            amountOfArguments = len(symbolTable)
            self.parent.counter += amountOfArguments
            for identifier, typename in symbolTable.items():
                typeAndAlign = llvm.checkTypeAndAlign(typename)
                localNumber = funcDef.getLocalNumber(typeAndAlign)
                # %4 = alloca i32, align 4
                file.write("%" + str(localNumber) + " = alloca " + str(typeAndAlign[0]) + ", align " + str(
                    typeAndAlign[1]) + "\n")
                # store i32 %0, i32* %4, align 4
                file.write("store " + str(typeAndAlign[0]) + " %" + str(localNumber - amountOfArguments - 1) + ", "
                           + str(typeAndAlign[0]) + "* %" + str(localNumber) + ", align " + str(typeAndAlign[1]) + "\n")
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
    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        if len(self.children) == 0:
            file.write("ret void\n")
        else:
            llvmReturnType = llvm.checkTypeAndAlign(funcDef.children[0].children[0].typename)[0]
            #####################################################################################################
            ######## DO NOT OPTIMIZE THE FOLLOWING CODE => Else the order of the writing won't be good!! ########
            #####################################################################################################
            file.write("ret " + str(llvmReturnType) + " " + str(
                self.children[0].toLLVM(file, funcDef, codeBody, llvmReturnType)) + "\n")
        # Return in llvm uses a register, so add 1 to the counter
        funcDef.getLocalNumber(llvm.checkTypeAndAlign('return'))


class DereferenceNode(ASTNode):  # TODO: llvm test
    def __init__(self):
        ASTNode.__init__(self)
        self.dereference = ''

    def processToken(self, token):
        self.dereference += token

    def text(self):
        return str(self.dereference)

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.dereference + '"];\n'

    def type(self):
        identifier = self.dereference[1:]
        type = symbolTables[-1].getEntry(identifier)
        return type + '*'

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        temp = llvm.getLLVMOfCVarible(self.dereference[1:len(self.dereference)], funcDef, codeBody)
        varName = temp[0]
        typeAndAlign = temp[1]
        if returnType is None:
            return llvm.changeLLVMType(str(typeAndAlign[0]) + '*', varName, funcDef, file)
        else:
            return llvm.changeLLVMType(returnType, varName, funcDef, file)



class DepointerNode(ASTNode):  # TODO: llvm test
    def __init__(self):
        ASTNode.__init__(self)
        self.depointer = ''

    def processToken(self, token):
        self.depointer += token

    def text(self):
        return self.depointer

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.depointer + '"];\n'

    def startDFS(self):
        identifier = self.depointer.split('*')[-1]
        type = symbolTables[-1].getEntry(identifier)
        if type.count('*') < self.depointer.count('*'):
            self.throwError("Indirection requires pointer operand ('{}' invalid)".format(type.split('*')[0]))

    def type(self):
        identifier = self.depointer.split('*')[-1]
        type = symbolTables[-1].getEntry(identifier)
        type = type.split('*')[0] + (type.count('*') - self.depointer.count('*')) * '*'
        return type

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        depointerAmount = 0
        for i in range(len(self.depointer)):
            if self.depointer[i] == '*':
                depointerAmount += 1
            if self.depointer[i] != '*':
                break
        var = llvm.getValueOfVariable(self.depointer[depointerAmount:len(self.depointer)], funcDef, codeBody, file)
        for _ in range(depointerAmount):
            var = llvm.getValueOfVariable(var, funcDef, codeBody, file)

        if returnType is None:
            return var
        else:
            return llvm.changeLLVMType(returnType, var, funcDef, file)



class ElseStatementNode(ASTNode):
    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        self.children[0].toLLVM(file, funcDef, codeBody)


class IfStatementNode(ASTNode):
    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        ELSE = len(self.children) == 3
        resultLLVMVar = self.children[0].toLLVM(file, funcDef, codeBody)
        # If the llvm var isn't the result from comparison, we have to see if it's zero or not
        if not isinstance(self.children[0], ComparisonNode):
            resultLLVMVar = llvm.writeLLVMCompareWithZero(resultLLVMVar, funcDef, file)

        # typeAndAlign1 = llvm.checkTypeAndAlign('label')
        # label1 = funcDef.getLocalNumber(typeAndAlign1)
        global labelCounter  # TODO: llvm: niet met global counter werken maar deel van de if statement nemen voor naam
        labelCounter += 1
        label1 = 'something' + str(labelCounter)

        # The order of the localNumbers has to be good, so pre-write the codeBody of the if statement
        tempFile1 = llvm.FileLookALike()
        self.children[1].toLLVM(tempFile1, funcDef, codeBody)  # TODO: llvm: weghalen tempfile en op juiste plaats zetten

        # typeAndAlign2 = llvm.checkTypeAndAlign('label')
        # label2 = funcDef.getLocalNumber(typeAndAlign2)
        labelCounter += 1
        label2 = 'something' + str(labelCounter)

        # Check if there's an else statement, if so also pre-write the codeBody of the else statement
        label3 = 'ERROR'
        tempFile2 = 'ERROR'
        if ELSE:
            # typeAndAlign3 = llvm.checkTypeAndAlign('label')
            # label3 = funcDef.getLocalNumber(typeAndAlign2)
            labelCounter += 1
            label3 = 'something' + str(labelCounter)

        # br i1 %5, label %6, label %8
        file.write('br i1 ' + str(resultLLVMVar) + ', label %' + str(label1) + ', label %' + str(label2) + '\n\n')
        # ; <label>:6:
        # file.write('; <label>:' + str(label1) + ':\n')
        file.write(label1 + ':\n')
        # codeBody of the if statement
        file.write(tempFile1.text)
        if ELSE:
            # br label %10
            file.write('br label %' + str(label3) + '\n\n')
        else:
            # br label %8
            file.write('br label %' + str(label2) + '\n\n')
        # ; <label>:8:
        # file.write('\n; <label>:' + str(label2) + ':\n')
        file.write(label2 + ':\n')
        if ELSE:
            # codeBody of the else statement
            self.children[2].toLLVM(file, funcDef, codeBody)
            # file.write(tempFile2.text)
            # br label %10
            file.write('br label %' + str(label3) + '\n\n')
            # ; <label>:10:
            # file.write('\n; <label>:' + str(label3) + ':\n')
            file.write(label3 + ':\n')



class WhileStatementNode(ASTNode):
    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        global labelCounter  # TODO: llvm: niet met global counter werken maar deel van de if statement nemen voor naam
        labelCounter += 1
        label1 = 'something' + str(labelCounter)
        # br label %something1  (while check)
        file.write('br label %' + str(label1) + '\n\n')

        # something1:  (check statement)
        file.write(label1 + ':\n')
        resultLLVMVar = self.children[0].toLLVM(file, funcDef, codeBody)
        # If the llvm var isn't the result from comparison, we have to see if it's zero or not
        if not isinstance(self.children[0], ComparisonNode):
            resultLLVMVar = llvm.writeLLVMCompareWithZero(resultLLVMVar, funcDef, file)

        labelCounter += 1
        label2 = 'something' + str(labelCounter)
        labelCounter += 1
        label3 = 'something' + str(labelCounter)

        # br i1 %3, label %something2, label %something3
        file.write('br i1 ' + str(resultLLVMVar) + ', label %' + str(label2) + ', label %' + str(label3) + '\n\n')

        # something2:  (while true)
        file.write(label2 + ':\n')
        self.children[1].toLLVM(file, funcDef, codeBody)
        # br label %something1  (while check)
        file.write('br label %' + str(label1) + '\n\n')

        # something3:  (stop while)
        file.write(label3 + ':\n')


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
        typename = self.children[0].typename
        identifier = self.children[1].identifier
        if identifier in reservedWords:
            self.throwError("Invalid usage of reserved keyword {}  as identifier ".format(identifier))
        symbolTables[-1].addSymbol(typename, identifier)

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        typeAndAlign = llvm.checkTypeAndAlign(self.children[0].typename)
        localNumber = funcDef.getLocalNumber(typeAndAlign)
        identifier = self.children[1].identifier
        codeBody.counterTable[identifier] = localNumber  # Link the C var and localNumber with each other
        # %2 = alloca i32, align 4
        file.write("%" + str(localNumber) + " = alloca " + str(typeAndAlign[0]) + ", align " + str(
            typeAndAlign[1]) + "\n")
        if len(self.children) == 3:
            # store i32 %3, i32* %2, align 4
            file.write("store " + str(typeAndAlign[0]) + " " + str(self.children[2].toLLVM(file, funcDef, codeBody, typeAndAlign[0])) + ", " + str(
                typeAndAlign[0]) + "* %" + str(localNumber) + ", align " + str(typeAndAlign[1]) + "\n")


class ArrayDeclarationNode(ASTNode):  # TODO: llvm
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
        typename = self.children[0].typename
        identifier = self.children[1].identifier
        size = ' '
        if len(self.children) == 4:
            size = self.children[2].value
            for child in self.children[3].children:
                self.compatibleInitializerTypes(typename, child.type())

        if len(self.children) == 3:
            if isinstance(self.children[2], ArrayListNode):
                size = len(self.children[2].children)
                for child in self.children[3].children:
                    self.compatibleInitializerTypes(typename, child.type())
            else:
                size = self.children[2].value
        typename = typename + '[' + str(size) + ']'

        if identifier in reservedWords:
            self.throwError("Invalid usage of reserved keyword {}  as identifier ".format(identifier))
        symbolTables[-1].addSymbol(typename, identifier)


class ConstantDeclarationNode(DeclarationNode):
    def startDFS(self):
        typename = self.children[0].typename
        if isinstance(self.children[1], IdentifierNode):
            identifier = self.children[1].identifier
        else:
            identifier = self.children[1].children[0].identifier
        if identifier in reservedWords:
            self.throwError('Invalid usage of reserved keyword {}  as identifier '.format(identifier))
        symbolTables[-1].addSymbol(typename, identifier)

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        typeAndAlign = llvm.checkTypeAndAlign(self.children[0].typename)
        if isinstance(self.parent, ProgramNode):
            if isinstance(self.children[1], IdentifierNode):
                if llvm.isPointer(typeAndAlign[0]):
                    standardValue = 'null'
                elif typeAndAlign[0] == 'float':
                    standardValue = '0x0000000000000000'
                else:
                    standardValue = '0'
                # @a = common global i32 0, align 4
                identifier = self.children[1].identifier
                file.write(
                    '@' + str(identifier) + ' = common global ' + str(typeAndAlign[0]) + ' ' + str(standardValue) + ', align ' +
                    typeAndAlign[1] + '\n')

            else:
                identifier = self.children[1].children[0].identifier
                file.write('@' + str(identifier) + ' = global ' + str(typeAndAlign[0]) + ' ')
                if llvm.isPointer(typeAndAlign[0]):
                    toBeReferenced = self.children[1].children[1].dereference
                    toBeReferenced = toBeReferenced[1:len(toBeReferenced)]
                    typeAndAlignRef = self.parent.typeAndAlignTable[toBeReferenced]
                    if typeAndAlignRef[0] + '*' == typeAndAlign[0]:
                        # @a1 = global i32* @a, align 8
                        file.write('@' + str(toBeReferenced))
                    else:
                        # @f1 = global i8* bitcast (float* @h to i8*), align 8
                        file.write('bitcast (' + str(typeAndAlignRef[0]) + '* @' + str(toBeReferenced) + ' to ' + str(typeAndAlign[0]) + ')')
                else:
                    # @a = global i32 5, align 4
                    file.write(str(llvm.valueTransformer(self.children[0].typename, self.children[1].children[1].value)))
                file.write(', align ' + typeAndAlign[1] + '\n')

            self.parent.typeAndAlignTable[identifier] = typeAndAlign
        elif isinstance(self.parent, CodeBodyNode):
            # %1 = alloca i32, align 4
            localNumber = funcDef.getLocalNumber(typeAndAlign)
            file.write('%' + str(localNumber) + ' = alloca ' + str(typeAndAlign[0]) + ', align ' + str(
                typeAndAlign[1]) + '\n')
            if isinstance(self.children[1], IdentifierNode):
                identifier = self.children[1].identifier
            else:
                identifier = self.children[1].children[0].identifier
                # store i32 3, i32* %1, align 4
                if isinstance(self.children[1].children[1], DereferenceNode):  # TODO: llvm: pointers
                    print("")
                file.write('store ' + str(typeAndAlign[0]) + ' ' + str(
                    llvm.valueTransformer(self.children[0].typename, self.children[1].children[1].value)) + ', ' + str(
                    typeAndAlign[0]) + '* %' + str(localNumber) + ', align ' + str(typeAndAlign[1]) + '\n')
            codeBody.counterTable[identifier] = localNumber  # Link the C var and localNumber with each other


class ConstantArrayDeclarationNode(ArrayDeclarationNode):  # TODO: llvm
    pass


class ConstantValueNode(ASTNode):
    pass


class ConstantNode(ASTNode):
    pass


class ArrayListNode(ASTNode):  # TODO: llvm
    pass


class ConstantArrayListNode(ArrayListNode):  # TODO: llvm
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

        functionTable.addFunction(typename, identifier, arguments, False)

    def endDFS(self):
        # symbol table is finished, pop from stack
        self.symbolTable = symbolTables.pop()

        # This is a function declaration in a function definition
        # We need to push all symbolTable entries back a level
        if len(symbolTables) > 1:
            symbolTables[-1] = self.symbolTable
        self.symbolTable = None

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        typeAndAsign = llvm.checkTypeAndAlign(self.children[0].typename)
        declaration = False
        file.write("\n")
        if isinstance(self.parent, FunctionDefinitionNode):
            file.write("define ")
        else:
            declaration = True
            file.write("declare ")
        if typeAndAsign[0] == "i8":
            file.write("signext ")
        file.write(str(typeAndAsign[0]) + " @" + str(self.children[1].identifier + "("))
        if len(self.children) == 2:
            # define i32 @main()
            file.write(")")
        elif len(self.children) == 3:
            # define void @f1(i32)
            for i in range(0, len(self.children[2].children) - 1, 2):
                typeAndAsign = llvm.checkTypeAndAlign(self.children[2].children[i].typename)
                if i != 0:
                    file.write(", ")
                file.write(str(typeAndAsign[0]))
                if typeAndAsign[0] == "i8":
                    file.write(" signext")
            file.write(") ")
        if declaration:
            file.write("\n")


class ArgumentDeclarationListNode(ASTNode):
    def startDFS(self):
        for i in range(0, len(self.children)):
            typename = None
            identifier = None
            if isinstance(self.children[i], ArrayTypeNode):  # Werkt alleen voor one dimensional arrays
                typename = self.children[i].children[0].typename + '*'
                identifier = self.children[i].children[1].identifier
            elif isinstance(self.children[i], TypeNameNode):
                typename = self.children[i].typename
                identifier = self.children[i+1].identifier

            if typename is None:
                continue

            if identifier in reservedWords:
                self.throwError("Invalid usage of reserved keyword {}  as identifier ".format(identifier))
            symbolTables[-1].addSymbol(typename, identifier)


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
        
        # TODO: check return type values
        
    def endDFS(self):
        # symbol table is finished, pop from stack
        identifier = self.children[0].children[1].identifier
        entry = functionTable.functionTable[identifier]
        functionTable.functionTable[identifier] = (entry[0], entry[1], True)
        self.symbolTable = symbolTables.pop()

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        # LLVM output part 1 here
        for child in self.children:
            child.toLLVM(file, self)
        # LLVM output part 2 here


class ReturnTypeNode(TypeNameNode):
    pass


class ArrayElementNode(ASTNode):  # TODO: llvm
    def type(self):
        identifier = self.children[0].identifier
        type = symbolTables[-1].getEntry(identifier)
        return type.split('[')[0]  # simplistic approach, only works for one dimensional arrays


class AssignmentNode(ASTNode):
    def startDFS(self):
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
        llvm.writeLLVMStoreForCVariable(self.children[0].identifier, self.children[1].toLLVM(file, funcDef, codeBody), funcDef, codeBody, file)


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
            self.fraction = int(token)
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
        return "'" + self.value + "'"

    def type(self):
        return 'char'


class FunctionCallNode(ASTNode):

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
        elif lhsType.count('*') > 0 and lhsType.split('*')[0] != rhsType.split('*')[0]:
            self.printWarning("Incompatible pointer types passing {} to parameter of type {}".format(rhsType, lhsType))

    def startDFS(self):
        identifier = self.children[0].identifier
        if not functionTable.exists(identifier):
            self.throwError("Identifier {} not found".format(identifier))
        if not functionTable.isDefined(identifier):
            self.throwError("Function {} is not defined".format(identifier))

        argumentCount = len(self.children[1].children)
        f = functionTable
        arguments = functionTable.functionTable[identifier][1]

        if argumentCount > len(arguments):
            self.throwError("Expected {} arguments, got {}".format(len(arguments), argumentCount))

        if arguments[-1] == '...':
            # infinite arguments possible
            if argumentCount < len(arguments) - 1:
                self.throwError("Expected at least {} arguments, got()".format(len(arguments) - 1, argumentCount))

            for i in range(len(arguments) - 1):  # Don't check the optional arguments
                self.compatibleArgumentTypes(arguments[i], self.children[1].children[i].type())

        else:
            if argumentCount < len(arguments):
                self.throwError("Expected {} arguments, got {}".format(len(arguments), argumentCount))
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

        for i in range(len(argumentTypes)):
            loc = self.children[1].children[i].toLLVM(file, funcDef, codeBody)
            arguments.append(llvm.changeLLVMType(llvm.checkTypeAndAlign(argumentTypes[i])[0], loc, funcDef, file))

        localNumber = 'ERROR'
        typeAndAsign = llvm.checkTypeAndAlign(returnType)
        if returnType != 'void':
            localNumber = funcDef.getLocalNumber(typeAndAsign)
            # %8 = call signext i8 @f1(i32 %5, i8 signext %7)
            file.write('%' + str(localNumber) + ' = ')
        file.write('call ')
        if typeAndAsign[0] == 'i8':
            file.write('signext ')
        file.write(str(typeAndAsign[0]) + ' @' + str(self.children[0].identifier + '('))
        if len(arguments) == 0:
            # call void @f2()
            file.write(')\n')
        else:
            # call void @f2(int %2, int %3)
            for i in range(len(argumentTypes)):
                typeAndAsign = llvm.checkTypeAndAlign(argumentTypes[i])
                if i != 0:
                    file.write(', ')
                file.write(str(typeAndAsign[0]))
                if typeAndAsign[0] == 'i8':
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
        self.throwError('Invalid types for binary operator {} : {}, {}'.format(self.operator, type1, type2))

    def mergeType(self, tpye1, type2):
        raise Exception("Not implemented for class {}".format(self.__class__))

    def mergeOperands(self, operands):
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
                newChildren.append(self.mergeOperands(temp))
                newChildren.append(self.children[i])
                temp = []
        if len(temp) > 0:
            newChildren.append(self.mergeOperands(temp))
        self.children.clear()
        if len(newChildren) == 1:
            index = self.parent.children.index(self)
            self.parent.children[index] = newChildren[0]
            self.parent.children[index].parent = self.parent
        else:
            for node in newChildren:
                self.add(node)


    def endDFS(self):
        self.foldExpression()

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):  # TODO: llvm: operations with pointers -> i64!!  TESTEN
        llvmTokens = list()
        llvmReturnType = ''
        it = 0
        # If one of the children is a dereference, always use the i64 type
        for child in self.children:
            if isinstance(child, DereferenceNode):
                llvmReturnType = 'i64'
                it = 1
                break
        if it == 1:
            pass
        # If the expression is part of an assignment or declaration, return the type of that variable
        elif isinstance(self.parent, AssignmentNode):
            it = 1
            llvmReturnType = llvm.getLLVMTypeOfCVariable(self.parent.children[0].identifier, funcDef, codeBody)
        elif isinstance(self.parent, DeclarationNode):
            it = 1
            llvmReturnType = llvm.getLLVMTypeOfCVariable(self.parent.children[1].identifier, funcDef, codeBody)
        for child in self.children:
            # If none of the statements before were true, take the type of the first operand
            if it == 0:
                if isinstance(self.children[0], ValueNode):
                    llvmTokens.append(child.value)
                    llvmReturnType = child.type()
                else:
                    llvmTokens.append(child.toLLVM(file, funcDef, codeBody))
                    llvmReturnType = llvm.getLLVMTypeOfLLVMVariable(llvmTokens[0], funcDef)
                it = 1
                continue
            llvmTokens.append(child.toLLVM(file, funcDef, codeBody, llvmReturnType))
        return llvmReturnType, llvmTokens


class SumNode(OperationNode):
    def isCompatibleType(self, type1, type2):
        if type1 in ['int', 'float', 'char'] and type2 in ['int', 'float', 'char']:
            return True
        if self.operator == '+' and (type1 in ['int', 'char'] and type2[-1] == '*'
                                     or type1[-1] == '*' and type2 in ['int', 'char']):
            return True
        if self.operator == '-' and type1[-1] == '*' and type2 in ['int', 'char']:
            return True
        self.throwError('Invalid types for binary operator {} : {}, {}'.format(self.operator, type1, type2))

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
        temp = []
        for child in self.children:
            if isinstance(child, ValueNode):
                temp.append(child)

        result = self.mergeOperands(temp)
        result.parent = self.parent
        if len(temp) != 0 and temp[0] == self.children[0]:
            # Result moet eerst in de children
            self.children[0] = result
        else:
            # Result moet laatst in de children
            self.children.append(result)

        for child in self.children:
            if isinstance(child, ValueNode) and child in temp:
                self.children.remove(child)

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        temp = super(SumNode, self).toLLVM(file, funcDef, codeBody)
        llvmReturnType = temp[0]
        operands = temp[1]

        llvmOperator = 'ERROR'
        if llvmReturnType == 'i32' or llvmReturnType == 'i8':
            if self.operator == '+':
                llvmOperator = 'add nsw'
            elif self.operator == '-':
                llvmOperator = 'sub nsw'
        elif llvmReturnType == 'float':
            if self.operator == '+':
                llvmOperator = 'fadd'
            elif self.operator == '-':
                llvmOperator = 'fsub'
        else:
            raise Exception('Unknown operator found!')

        if returnType is None:
            return llvm.writeLLVMOperation(llvmOperator, llvmReturnType, operands, funcDef, file)
        else:
            return llvm.writeLLVMOperation(returnType, llvmReturnType, operands, funcDef, file)


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

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        temp = super(ProductNode, self).toLLVM(file, funcDef, codeBody)
        llvmReturnType = temp[0]
        operands = temp[1]

        llvmOperator = 'ERROR'
        if llvmReturnType == 'i32' or llvmReturnType == 'i8':
            if self.operator == '*':
                llvmOperator = 'mul nsw'
            elif self.operator == '/':
                llvmOperator = 'sdiv'
        elif llvmReturnType == 'float':
            if self.operator == '*':
                llvmOperator = 'fmul'
            elif self.operator == '/':
                llvmOperator = 'fdiv'
        else:
            raise Exception('Unknown operator found!')

        if returnType is None:
            return llvm.writeLLVMOperation(llvmOperator, llvmReturnType, operands, funcDef, file)
        else:
            return llvm.writeLLVMOperation(returnType, llvmReturnType, operands, funcDef, file)


class ComparisonNode(OperationNode):
    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        temp = super(ComparisonNode, self).toLLVM(file, funcDef, codeBody)
        llvmReturnType = temp[0]
        operands = temp[1]

        llvmOperator = 'ERROR'
        if llvmReturnType == 'i32' or llvmReturnType == 'i8':
            if self.operator == '==':
                llvmOperator = 'icmp eq'
            elif self.operator == '<':
                llvmOperator = 'icmp slt'
            elif self.operator == '>':
                llvmOperator = 'icmp sgt'
        elif llvmReturnType == 'float':
            if self.operator == '==':
                llvmOperator = 'fcmp oeq'
            elif self.operator == '<':
                llvmOperator = 'fcmp olt'
            elif self.operator == '>':
                llvmOperator = 'fcmp ogt'
        else:
            raise Exception('Unknown operator found!')

        if returnType is None:
            return llvm.writeLLVMOperation(llvmOperator, llvmReturnType, operands, funcDef, file, True)
        else:
            return llvm.writeLLVMOperation(returnType, llvmReturnType, operands, funcDef, file, True)


class ConstantComparisonNode(OperationNode):
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
        if symbolTables[-1].exists(self.identifier):
            return symbolTables[-1].getEntry(self.identifier)

    def toLLVM(self, file, funcDef=None, codeBody=None, returnType=None):
        if returnType is None:
            return llvm.getValueOfVariable(self.identifier, funcDef, codeBody, file)
        else:
            return llvm.valueTransformer(returnType, llvm.getValueOfVariable(self.identifier, funcDef, codeBody, file))
