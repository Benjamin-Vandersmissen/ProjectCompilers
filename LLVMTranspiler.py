import llvm
from ExpressionTree import *
import copy

printf = '''
printf:
move $t0, $a0 
move $t1, $a1 
sll $t1, $t1, 2 
li $t2, 0 

p_processChar:
addu $t3, $t0, $t2 
lw, $t3, ($t3) 
addi $t2, $t2, 4 
beq $t3, 0, endPrint 
beq $t3, 37, p_percent
move $a0, $t3
li $v0, 11
syscall
b p_processChar 

p_percent:
addu $t3, $t0, $t2
lw $t3, ($t3)
addi $t2, $t2, 4
la $t4, ($sp)
addu $t4, $t4, $t1
subu $t1, $t1, 4
lw $a0, ($t4) 
beq $t3, 0, endPrint
beq $t3, 105, printInt
beq $t3, 102, printFloat
beq $t3, 99, printChar
la $a0, error
li $v0, 4
syscall
move $a0, $t4
li $v0, 11
syscall
li $v0, 10
syscall

printInt:
li $v0, 1
syscall
b p_processChar

printFloat:
mtc1 $a0, $f12
li $v0, 2
syscall
b p_processChar

printChar:
li $v0, 11
syscall
b p_processChar

endPrint:
jr $ra
'''

scanf = '''
scanf:
move $t0, $a0 
move $t1, $a1 
sll $t1, $t1, 2
li $t2, 0

s_processChar:
addu $t3, $t0, $t2
lw, $t3, ($t3) 
addi $t2, $t2, 4
beq $t3, 0, endScan 
beq $t3, 37, s_percent
b s_processChar 

s_percent:
addu $t3, $t0, $t2
lw $t3, ($t3)
addi $t2, $t2, 4
la $t4, ($sp)
addu $t4, $t4, $t1
subu $t1, $t1, 4
lw $t4, ($t4) 
beq $t3, 0, endScan
beq $t3, 105, scanInt 
beq $t3, 102, scanFloat
beq $t3, 99, scanChar
la $a0, error
li $v0, 4
syscall
move $a0, $t4
li $v0, 11
syscall
li $v0, 10
syscall

scanInt:
li $v0, 5
syscall
sw $v0, ($t4)
b s_processChar

scanFloat:
mtc1 $a0, $f12
li $v0, 6
syscall
swc1 $f0, ($t4)
b s_processChar

scanChar:
li $v0, 12
syscall
sw $v0, ($t4)
b s_processChar

endScan:
jr $ra
'''


def extractVars(tokens):
    vars = []
    for token in tokens:
        if token[0] == '%':
            vars.append(token)
    return vars


def tokenise(line):
    tokens = line.split()
    temp = []
    for i in range(len(copy.copy(tokens))):
        token = tokens[i]
        token = token.split(',')[0]
        token = token.split(')')[0]
        if '(' in token:
            temp += token.split('(')
        else:
            temp.append(token)
    temp = [token for token in temp if token != '']
    return temp


class Stack:
    def __init__(self):
        self._stack = []
        self._pointers = dict()
        self.temporaries = dict()
        self._variables = dict()
        # Aantal argumenten in deze scope,
        # stel dat er registers gerefereerd worden die nooit gestored zijn, dan kunnen dit argumenten zijn
        self._arguments = 0


    def allocate(self, variable):
        self._variables[variable] = '$s{}'.format(len(self._variables))

    def allocateArray(self, variable, size):
        for i in range(int(size)):
            self._stack.append(variable)

    def allocateTemp(self, variable):
        self.temporaries[variable] = '$t{}'.format(len(set(self.temporaries.values())))

    def clearTemporaries(self):
        self.temporaries = {}

    def position(self, variable):
        if variable[0] == '@':  # global variable
            return variable

        if variable in self.temporaries:
            return self.temporaries[variable]

        elif variable in self._variables:
            return self._variables[variable]

        elif variable in self._stack:
            return '{}($sp)'.format(4 * (1 + self._stack.index(variable)))

        elif variable in self._pointers:
            pointee, offset = self._pointers[variable]

            # Find occurence (offset + 1) in the stack
            return '{}($sp)'.format(4 * (1 + [i for i, n in enumerate(self._stack) if n == pointee][offset]))

        elif int(variable[1:]) < self._arguments:
            offset = (self._arguments - int(variable[1:])) * 4
            return '{}($fp)'.format(offset)

    def push(self, register):
        self._stack.append(register)

    def pop(self, register):
        self._stack.pop()

    def add_pointer(self, pointer, pointee, offset=0):
        offset = int(offset)
        while pointee not in self._stack:
            pointee, increase = self._pointers[pointee]
            offset += increase
        self._pointers[pointer] = pointee, offset

    def offset(self, register):
        offset = 0
        if register in self._pointers:
            register, offset = self._pointers[register]
        list = [i for i, n in enumerate(self._stack) if n == register]
        if len(list) <= offset:
            return -1
        return 4 * (len(self._stack) - list[offset])

    def storeVariables(self):
        retvalue = ""
        i = 0
        for temp in set(self.temporaries.values()):
            retvalue += "sw {}, -{}($sp)\n".format(temp, i)
            i += 4
        for var in set(self._variables.values()):
            retvalue += "sw {}, -{}($sp)\n".format(var, i)
            i += 4
        retvalue += "subu $sp, $sp, {}\n\n".format(i)
        return retvalue

    def loadVariables(self):
        retValue = ""
        i = 0
        for var in reversed(list(set(self._variables.values()))):
            i += 4
            retValue += "lw {}, {}($sp)\n".format(var, i)

        for temp in reversed(list(set(self.temporaries.values()))):
            i += 4
            retValue += "lw {}, {}($sp)\n".format(temp, i)
        retValue += "addu $sp, $sp, {}\n\n".format(i)
        return retValue


class LLVMTranspiler:
    def __init__(self, filename):
        self._llvmFile = open(filename, "r")
        self._mipsFile = open(filename.split('.ll')[0] + '.asm', "w+")
        self._textFragment = ''
        self._dataFragment = ''
        self._positiontables = []
        self._IOdefined = False

    def consumeUntil(self, line, tokens):
        retvalue, line = line.split(tokens, 1)
        return retvalue, line

    def getGlobalName(self, variable):
        if variable[0] == '@':
            return '_' + variable[1:]
        else:
            raise Exception("Ge moet hier nie zijn")  # TODO: pas dit zeker niet aan

    def loadFloatImmediate(self, tempregister, floatregister, hexFloat):
        float = hexFloat[:-8]
        retvalue = 'li {}, {}\n'.format(tempregister, float)
        retvalue += 'sw {}, -4($sp)\n'.format(tempregister)
        retvalue += 'lwc1 {}, -4($sp)\n'.format(floatregister)
        return retvalue

    def createTextFragment(self):
        self._textFragment += '\n.text\n'
        self._textFragment += 'jal _main\n'
        self._textFragment += 'li $v0 10\n'  # Exit the program responsibly
        self._textFragment += 'syscall\n'

    def globalAssignment(self, tokens):
        global_variable = self.getGlobalName(tokens[0])
        type = tokens[3]

        if type[0] == '[':  # Array type
            if 'float' in tokens[5]:
                type = '.float'
            else:
                type = '.word'
            self._dataFragment += '{}: {} '.format(global_variable, type)
            for i in range(7, len(tokens) - 2, 2):
                value = tokens[i].split(']')[0]
                if type == '.float':
                    value - llvm.hex_to_float(value)

                if i > 7:
                    self._dataFragment += ', '
                self._dataFragment += '{}'.format(value)
            self._dataFragment += '\n'
            return

        value = tokens[4]
        if type == 'float':
            type = '.float'
            value = llvm.hex_to_float(value)
        else:
            type = '.word'
        self._dataFragment += '{}: {} {}\n'.format(global_variable, type, value)

    def functionDefinition(self, tokens):
        # Argumenten worden opgeslagen op de stack

        self._positiontables.append(Stack())
        name = self.getGlobalName(tokens[2])
        self._textFragment += '\n{}:\n'.format(name)
        self._textFragment += 'sw $fp, ($sp) \nmove $fp, $sp \nsubu $sp, $sp, 8 \nsw $ra, -4($fp)\n\n'

        argumentSize = len(tokens) - 4
        self._positiontables[-1]._arguments = argumentSize

    def restorePtrs(self):
        self._textFragment += 'lw $ra, -4($fp) \nmove $sp, $fp \nlw $fp, ($sp)\n'
        self._textFragment += 'jr $ra\n'


    def convertTo32bitFloat(self, value):
        # value is in string representation
        value = value[:-8]
        return value

    def allocate(self, tokens):
        register = tokens[0]
        if '[' in tokens[3]:  # array
            # TODO: float ?
            self._positiontables[-1].allocateArray(register, tokens[3][1:])
            self._textFragment += 'subu $sp, $sp, {}\n'.format(4 * int(tokens[3][1:]))
        else:
            self._positiontables[-1].allocate(register)

    def store(self, tokens):
        value = tokens[2]
        register = tokens[4]
        to_register = self._positiontables[-1].position(register)
        if '%' in value:
            from_register = self._positiontables[-1].position(value)
            if '$fp' in from_register:
                self._textFragment += 'lw {}, {}\n'.format(to_register, from_register)
            else:
                self._textFragment += 'move {}, {}\n'.format(to_register, from_register)
        else:
            # TODO: float
            if '$sp' in to_register:
                # use v1 for temporary immediate loading
                self._textFragment += 'li $v1, {}\n'.format(value)
                self._textFragment += 'sw $v1, {}\n'.format(to_register)
            else:
                self._textFragment += 'li {}, {}\n'.format(to_register, value)

        self._positiontables[-1].clearTemporaries()

    def makePointer(self, tokens):
        variables = [token for token in tokens if token[0] == '%']
        to_register = variables[0]
        from_register = variables[1]
        offset = tokens[tokens.index(from_register) + 2]
        self._positiontables[-1].add_pointer(to_register, from_register, offset)

    def ret(self, tokens):
        if tokens[1] == 'void':
            pass
        elif tokens[2][0] == '%':
            from_register = self._positiontables[-1].position(tokens[2])
            self._textFragment += 'move $v0, {}\n'.format(from_register)
        elif tokens[2][0] == '@':
            var = self.getGlobalName(tokens[2])
            self._textFragment += 'lw $v0, {}\n'.format(var)
        else:
            self._textFragment += 'li $v0, {}\n'.format(tokens[2])

        self.restorePtrs()

    def call(self, tokens):
        identifier = [token for token in tokens if token[0] == '@'][0]
        parameters = []

        if identifier == '@printf' and self._IOdefined:
            string_position = self._positiontables[-1].position(tokens[tokens.index(identifier) + 2])
            self._textFragment += 'la $a0, {}\n'.format(string_position)
            for j in range(tokens.index(identifier) + 4, len(tokens), 2):
                parameters.append(tokens[j])
            self._textFragment += 'li $a1, {}\n'.format(len(parameters))
            identifier = identifier[1:]

        elif identifier == '@scanf' and self._IOdefined:
            pass

        else:
            for j in range(tokens.index(identifier) + 2, len(tokens), 2):
                parameters.append(tokens[j])
            identifier = '_' + identifier[1:]

        self._textFragment += self._positiontables[-1].storeVariables()

        for j in range(len(parameters)):  # store parameters on stack
            stack_offset = -4 * j
            parameter = parameters[j]
            if parameter[0] == '%':
                from_register = self._positiontables[-1].position(parameter)
                self._textFragment += 'sw {}, {}($sp)\n'.format(from_register, stack_offset)
            elif parameter[0] == '@':  # TODO
                pass
            else:
                self._textFragment += 'li $v1, {}\n'.format(parameter)
                self._textFragment += 'sw $v1, {}($sp)\n'.format(stack_offset)

        self._textFragment += 'subu $sp, $sp, {}\n'.format(4 * len(parameters))
        self._textFragment += 'jal {}\n'.format(identifier)
        self._textFragment += 'addu $sp, $sp, {}\n'.format(4 * len(parameters))

        self._textFragment += self._positiontables[-1].loadVariables()

        if tokens[0] != 'call':  # save return value
            to_register = self._positiontables[-1].position(tokens[0])
            self._textFragment += 'move {}, $v0\n\n'.format(to_register)

    def operation(self, tokens):
        to_register = self._positiontables[-1].position(tokens[0])
        operator = tokens[2]
        value = tokens[5]
        if value[0] == '%':
            from_register = self._positiontables[-1].position(tokens[4])
            self._textFragment += '{} {}, {}, {}\n'.format(operator, to_register, to_register,
                                                           from_register)
        elif value[0] == '@':
            var = self.getGlobalName(value)
            self._textFragment += '{} {}, {}, {}\n'.format(operator, to_register, to_register, var)

        else:  # use immediate
            operator += 'i'
            self._textFragment += '{} {}, {}, {}\n'.format(operator, to_register, to_register, value)


    # Returns the index of the first line not belonging to this scope
    def processScope(self, lines, index):
        data = []
        retvalue = index
        for i in range(index, len(lines)):
            if lines[i] == '}':
                retvalue = i - 1
                break
            else:
                data.append(tokenise(lines[i]))

        i = -1
        while i < len(data) - 1:
            i += 1
            # TODO: overal speciale gevallen met globale variabelen/floats implementeren

            tokens = data[i]
            variables = [token for token in tokens if token[0] == '%']

            if len(tokens) == 0:
                continue

            elif tokens[0][-1] == ':':  # label
                self._textFragment += '{}\n'.format(tokens[0])

            elif tokens[0] == 'store':  # store variable
                self.store(tokens)

            elif tokens[0] == 'ret':
                self.ret(tokens)

            elif tokens[0] == 'call':  # function call without storing return
                self.call(tokens)

            elif tokens[0] == 'br':
                if tokens[1] == 'label':
                    self._textFragment += 'b {}\n\n'.format(tokens[2][1:])
                else:
                    condition = tokens[2]
                    cond_register = self._positiontables[-1].position(condition)
                    label_true = tokens[4][1:]
                    label_false = tokens[6][1:]
                    self._textFragment += 'bnez {}, {}\n'.format(cond_register, label_true)
                    self._textFragment += 'beqz {}, {}\n\n'.format(cond_register, label_false)

            elif tokens[2] == 'getelementptr':
                self.makePointer(tokens)

            elif tokens[2] == 'alloca':
                self.allocate(tokens)

            elif tokens[0] == variables[0]:
                # catch all voor operaties die returnwaarde teruggeven en met up to date registers moeten werken

                # Allocate temporary for variable
                if self._positiontables[-1].position(variables[0]) is None:
                    # variable heeft nog geen register ==> maak expression tree
                    expressions = []  # expressions voor in expression tree
                    for j in range(i, len(data)):
                        temp_vars = [token for token in data[j] if token[0] == '%']
                        if 'store' in data[j] or 'ret' in data[j] or 'br' in data[j]:  # expressie is hier volledig
                            break
                        elif len(temp_vars) == 3 and 'call' not in data[j]:
                            expressions.append(data[j])

                    if len(expressions) > 0:
                        tree = None
                        unused_expressions = [expr for expr in data[i:j] if expr not in expressions]
                        for k in range(1, len(expressions) + 1):
                            temp_tokens = expressions[-k]
                            temp_vars = [token for token in temp_tokens if token[0] == '%']
                            if tree is None:
                                tree = ExpressionTree(temp_vars[0], temp_vars[1], temp_vars[2], temp_tokens)
                            else:
                                if not tree.addNode(temp_vars[0], temp_vars[1], temp_vars[2], temp_tokens):
                                    raise Exception("Ge moet hier nie zijn")  # TODO: pas dit zeker niet aan

                        register_map = dict()
                        new_operations = []
                        if tree is not None:
                            tree.getErshovNumber()
                            basenumber = len(set(self._positiontables[-1].temporaries.values()))
                            register_map, new_operations = tree.getRegisters(basenumber)

                            if variables[0] in register_map:
                                # update temporaries alleen als het effect heeft op deze statement
                                self._positiontables[-1].temporaries.update(register_map)

                                # re-order operations
                                leftPart = data[:i]
                                rightPart = data[j:]
                                for expression in new_operations:
                                    leftPart.append(expression)
                                # insert unused expressions before the first used expression behind it
                                for expression in unused_expressions:
                                    index = data[i:j].index(expression)
                                    for k in range(index + 1, j):
                                        if data[i + k] in expressions:
                                            index = leftPart.index(data[i + k])
                                            leftPart = leftPart[:index] + [expression] + leftPart[index:]
                                            break

                                data = leftPart + rightPart
                                i = data.index(tokens) - 1
                                continue
                            else:
                                if len(variables) > 1 and 'call' not in tokens and 'load' not in tokens:
                                    # assign same temporary as other argument (for operations using an immediates)
                                    self._positiontables[-1].temporaries[variables[0]] = \
                                        self._positiontables[-1].temporaries[
                                            variables[1]]
                                else:
                                    self._positiontables[-1].allocateTemp(variables[0])
                    else:
                        if len(variables) > 1 and 'call' not in tokens and 'load' not in tokens:
                            # assign same temporary as other argument (for operations using an immediates)
                            self._positiontables[-1].temporaries[variables[0]] = self._positiontables[-1].temporaries[
                                variables[1]]
                        else:
                            self._positiontables[-1].allocateTemp(variables[0])

                if tokens[2] == 'add' or tokens[2] == 'sub' or tokens[2] == 'mul' or tokens[2] == 'div':
                    self.operation(tokens)

                elif tokens[2] == 'load':
                    if tokens[3][0] != '[':
                        # TODO: is dit een fix? En waaraom wordt er een load gedaan van een array vlak voor printf?
                        # TODO: zet in aparte functie
                        to_register = self._positiontables[-1].position(variables[0])
                        if len(variables) > 1:
                            from_register = self._positiontables[-1].position(variables[1])
                            self._textFragment += 'move {}, {}\n'.format(to_register, from_register)
                        else:
                            value = tokens[5]
                            self._textFragment += 'li {}, {}\n'.format(to_register, value)

                elif tokens[2] == 'call':
                    self.call(tokens)

                elif tokens[2] == 'icmp':
                    # TODO: zet in aparte functie
                    to_register = self._positiontables[-1].position(tokens[0])
                    comparator = tokens[3]
                    lhs = tokens[5]
                    rhs = tokens[6]
                    if comparator == 'eq':
                        comparator = 's' + comparator

                    lhs = self._positiontables[-1].position(lhs)
                    if rhs[0] == '%':
                        rhs = self._positiontables[-1].position(rhs)
                    self._textFragment += '{} {}, {}, {}\n'.format(comparator, to_register, lhs, rhs)

        return retvalue

    def transpile(self):
        self.createTextFragment()
        self._dataFragment += '.data\n'

        lines = self._llvmFile.read().split('\n')
        i = 0
        in_function = False
        while i < len(lines):
            line = lines[i]
            tokens = tokenise(line)
            if len(tokens) == 0:
                i += 1
                continue
            elif in_function:
                # process function scope
                i = self.processScope(lines, i)
                in_function = False

            elif tokens[0][0] == '@':
                # globale variable assignment
                self.globalAssignment(tokens)
            elif tokens[0] == 'define':
                # function definition
                self.functionDefinition(tokens)
                in_function = True
            elif tokens[0] == '}':
                self._positiontables.pop()

            elif tokens[0] == 'declare':
                if not self._IOdefined:
                    self._dataFragment += 'error: .asciiz "unrecognised parameter %"\n'
                if tokens[2] == '@printf':
                    self._textFragment += printf + '\n'
                if tokens[2] == '@scanf':
                    self._textFragment += scanf + '\n'
                self._IOdefined = True

            i += 1

        self._mipsFile.write(self._dataFragment)
        self._mipsFile.write(self._textFragment)
        self._mipsFile.close()
