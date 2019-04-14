import llvm

symbolTables = list()
reservedWords = ['if', 'else', 'return', 'while', 'char', 'int', 'float', 'void']


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

    # Create the llvm code for this node in the AST
    # expects file to be an opened writable file
    # expects fundDef to be a FuntionDefenitionNode. Only children from such a node, need this argument!!
    def toLLVM(self, file, funcDef=None):
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

    def startDFS(self):
        # build a new symbol table
        global symbolTables
        newSymbolTable = SymbolTableNode()
        symbolTables[-1].add(newSymbolTable)
        symbolTables.append(newSymbolTable)

    def endDFS(self):
        # symbol table is finished, pop from stack
        self.symbolTable = symbolTables.pop()

    def toLLVM(self, file, funcDef=None):
        func = isinstance(self.parent, FunctionDefinitionNode)
        file.write("{\n")
        # If a function body, add the arguments of the function
        if func:
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
                funcDef.counterTable[identifier] = localNumber  # Link the var and localNumber with each other
        returned = False
        for child in self.children:
            child.toLLVM(file, funcDef)
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
        file.write("}\n")


class StatementNode(ASTNode):
    pass


class ReturnStatementNode(ASTNode):
    def toLLVM(self, file, funcDef=None):
        if len(self.children) == 0:
            file.write("ret void\n")
        else:
            llvmReturnType = llvm.checkTypeAndAlign(funcDef.children[0].children[0].typename)[0]
            child = self.children[0]
            #####################################################################################################
            ######## DO NOT OPTIMIZE THE FOLLOWING CODE => Else the order of the writing won't be good!! ########
            #####################################################################################################
            if isinstance(child, ValueNode):
                file.write("ret " + str(llvmReturnType) + " " + str(
                    llvm.valueTransformer(llvmReturnType, self.children[0].value)) + "\n")
            else:
                file.write("ret " + str(llvmReturnType) + " " + str(
                    llvm.changeLLVMType(llvmReturnType, self.children[0].toLLVM(file, funcDef), funcDef, file)) + "\n")


class DereferenceNode(ASTNode):  # TODO: llvm
    def __init__(self):
        ASTNode.__init__(self)
        self.dereference = ''

    def processToken(self, token):
        self.dereference += token

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.dereference + '"];\n'

    def type(self):
        identifier = self.dereference[1:]
        type = symbolTables[-1].getEntry(identifier)
        return type + '*'


class DepointerNode(ASTNode):  # TODO: llvm
    def __init__(self):
        ASTNode.__init__(self)
        self.depointer = ''

    def processToken(self, token):
        self.depointer += token

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


class ElseStatementNode(ASTNode):  # TODO: llvm
    pass


class IfStatementNode(ASTNode):  # TODO: llvm
    pass


class WhileStatementNode(ASTNode):  # TODO: llvm
    pass


class TypeNameNode(ASTNode):

    def __init__(self):
        ASTNode.__init__(self)
        self.typename = ''

    def processToken(self, token):
        self.typename += token

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.typename + '"];\n'


class DeclarationNode(ASTNode):
    def startDFS(self):
        typename = self.children[0].typename
        identifier = self.children[1].identifier
        if identifier in reservedWords:
            self.throwError("Invalid usage of reserved keyword {}  as identifier ".format(identifier))
        symbolTables[-1].addSymbol(typename, identifier)

    def toLLVM(self, file, funcDef=None):
        typeAndAlign = llvm.checkTypeAndAlign(self.children[0].typename)
        localNumber = funcDef.getLocalNumber(typeAndAlign)
        identifier = self.children[1].identifier
        funcDef.counterTable[identifier] = localNumber  # Link the C var and localNumber with each other
        # %2 = alloca i32, align 4
        file.write("%" + str(localNumber) + " = alloca " + str(typeAndAlign[0]) + ", align " + str(
            typeAndAlign[1]) + "\n")
        if len(self.children) == 3:
            # store i32 %3, i32* %2, align 4
            file.write("store " + str(typeAndAlign[0]) + " " + str(self.children[2].toLLVM(file, funcDef)) + ", " + str(
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
            self.throwError("Invalid usage of reserved keyword {}  as identifier ".format(identifier))
        symbolTables[-1].addSymbol(typename, identifier)

    def toLLVM(self, file, funcDef=None):
        typeAndAlign = llvm.checkTypeAndAlign(self.children[0].typename)
        if isinstance(self.parent, ProgramNode):
            if isinstance(self.children[1], IdentifierNode):
                # @a = common global i32 0, align 4
                identifier = self.children[1].identifier
                file.write(
                    "@" + str(identifier) + " = common global " + str(typeAndAlign[0]) + " 0, align " +
                    typeAndAlign[1] + "\n")

            else:
                # @a = global i32 5, align 4
                identifier = self.children[1].children[0].identifier
                file.write("@" + str(identifier) + " = global " + str(
                    typeAndAlign[0]) + " " + str(
                    llvm.valueTransformer(self.children[0].typename, self.children[1].children[1].value)) + ", align " +
                           typeAndAlign[1] + "\n")
            self.parent.typeAndAlignTable[identifier] = typeAndAlign
        elif isinstance(self.parent, CodeBodyNode):
            # %1 = alloca i32, align 4
            localNumber = funcDef.getLocalNumber(typeAndAlign)
            file.write("%" + str(localNumber) + " = alloca " + str(typeAndAlign[0]) + ", align " + str(
                typeAndAlign[1]) + "\n")
            if isinstance(self.children[1], IdentifierNode):
                identifier = self.children[1].identifier
            else:
                identifier = self.children[1].children[0].identifier
                # store i32 3, i32* %1, align 4
                file.write("store " + str(typeAndAlign[0]) + " " + str(
                    llvm.valueTransformer(self.children[0].typename, self.children[1].children[1].value)) + ", " + str(
                    typeAndAlign[0]) + "* %" + str(localNumber) + ", align " + str(typeAndAlign[1]) + "\n")
            funcDef.counterTable[identifier] = localNumber  # Link the C var and localNumber with each other


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
        # TODO: recognise arrays as arguments

        if len(self.children) > 2:
            for i in range(0, len(self.children[2].children), 2):
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

    def toLLVM(self, file, funcDef=None):
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
        for i in range(0, len(self.children), 2):
            typename = self.children[i].typename
            identifier = self.children[i + 1].identifier
            if identifier in reservedWords:
                self.throwError("Invalid usage of reserved keyword {}  as identifier ".format(identifier))
            symbolTables[-1].addSymbol(typename, identifier)


class FunctionDefinitionNode(ASTNode):
    def __init__(self):
        super().__init__()
        self.counter = 1
        self.counterTable = dict()
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

    def toLLVM(self, file, funcDef=None):
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

    def toLLVM(self, file, funcDef=None):
        llvm.writeLLVMStoreForCVariable(self.children[0].identifier, self.children[1].toLLVM(file, funcDef), funcDef, file)


class ConstantAssignmentNode(AssignmentNode):  # TODO: in global scope folden in ConstantDeclaration, rest werkt (ook llvm)
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

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + \
               ('-' if self.sign < 0 else '') + str(self.value) + '"];\n'

    def type(self):
        return 'float'


class CharValueNode(ValueNode):

    def processToken(self, token):
        self.value = token[1]

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

    def toLLVM(self, file, funcDef=None):
        temp = funcDef.parent.functionTable.functionTable[self.children[0].identifier]
        returnType = temp [0]
        argumentTypes = temp[1]
        arguments = []

        for i in range(len(argumentTypes)):
            loc = self.children[1].children[i].toLLVM(file, funcDef)
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
            return '%' + str(localNumber)
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

    def canMerge(self, node):
        return ASTNode.canMerge(self, node) and node.operator == self.operator

    def dotRepresentation(self):
        return '\t"' + self.name() + '_' + str(self.id) + '"[label="' + self.operator + '"];\n'

    def toLLVM(self, file, funcDef=None):
        llvmTokens = list()
        llvmReturnType = ''
        it = 0
        for child in self.children:
            if it == 0:
                if isinstance(self.children[0], ValueNode):
                    llvmTokens.append(child.value)
                    if isinstance(self.children[0], IntValueNode):
                        llvmReturnType = 'i32'
                    elif isinstance(self.children[0], CharValueNode):
                        llvmReturnType = 'i8'
                    elif isinstance(self.children[0], FloatValueNode):
                        llvmReturnType = 'float'
                    else:
                        raise Exception('Non existing ValueNode type!')
                else:
                    llvmTokens.append(child.toLLVM(file, funcDef))
                    llvmReturnType = llvm.getLLVMTypeOfLLVMVariable(llvmTokens[0], funcDef)
                it += 1
                continue
            if isinstance(child, ValueNode) or child.__class__.__name__[0:8] == 'Constant':
                llvmTokens.append(llvm.valueTransformer(llvmReturnType, child.value))
            else:
                llvmTokens.append(llvm.changeLLVMType(llvmReturnType, child.toLLVM(file, funcDef), funcDef, file))
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

    def toLLVM(self, file, funcDef=None):
        temp = super(SumNode, self).toLLVM(file, funcDef)
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

        return llvm.writeLLVMOperation(llvmOperator, llvmReturnType, operands, funcDef, file)


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

    def toLLVM(self, file, funcDef=None):
        temp = super(ProductNode, self).toLLVM(file, funcDef)
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

        return llvm.writeLLVMOperation(llvmOperator, llvmReturnType, operands, funcDef, file)


class ComparisonNode(OperationNode):
    def toLLVM(self, file, funcDef=None):
        temp = super(ComparisonNode, self).toLLVM(file, funcDef)
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

        return llvm.writeLLVMOperation(llvmOperator, llvmReturnType, operands, funcDef, file, True)


class ConstantComparisonNode(OperationNode):
    pass


class ConstantSumNode(SumNode):
    def foldExpression(self):
        type = self.type()
        value = None
        for index in range(len(self.children)):
            child = self.children[index]
            if isinstance(child, ConstantSumNode) or isinstance(child, ConstantProductNode):
                child.foldExpression()
                child = self.children[index]
            if value is None:
                value = child.value
            elif self.operator == '+':
                if isinstance(child.value, str):
                    value += ord(child.value)
                else:
                    value += child.value
            elif self.operator == '-':
                if isinstance(child.value, str):
                    value -= ord(child.value)
                else:
                    value -= child.value

        index = self.parent.children.index(self)
        if type == 'float':
            self.parent.children[index] = FloatValueNode()
        if type == 'int':
            self.parent.children[index] = IntValueNode()
        if type == 'char':
            self.parent.children[index] = CharValueNode()

        self.parent.children[index].value = value
        self.parent.children[index].parent = self.parent

    def startDFS(self):
        self.foldExpression()


class ConstantProductNode(ProductNode):
    def foldExpression(self):
        type = self.type()
        value = None
        for index in range(len(self.children)):
            child = self.children[index]
            if isinstance(child, ConstantSumNode) or isinstance(child, ConstantProductNode):
                child.foldExpression()
                child = self.children[index]
            if value is None:
                value = child.value
            elif self.operator == '*':
                value *= child.value
            elif self.operator == '/':
                value /= child.value

        index = self.parent.children.index(self)
        if type == 'float':
            self.parent.children[index] = FloatValueNode()
        if type == 'int':
            self.parent.children[index] = IntValueNode()
        if type == 'char':
            self.parent.children[index] = CharValueNode()

        self.parent.children[index].value = value
        self.parent.children[index].parent = self.parent

    def startDFS(self):
        self.foldExpression()


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
            raise Exception(
                "Identifier " + self.identifier + " not found at " + str(self.line) + ":" + str(self.column))

    def type(self):
        if symbolTables[-1].exists(self.identifier):
            return symbolTables[-1].getEntry(self.identifier)

    def toLLVM(self, file, funcDef=None):
        return llvm.getValueOfCVariable(self.identifier, funcDef, file)
