import struct
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


def tokenise(line):
    tokens = line.split()
    temp = []
    for i in range(len(copy.copy(tokens))):
        token = tokens[i]
        token = token.split(',')[0]
        token = token.split(')')[0]
        if '0x' in token:  # trim float
            token = token[:-8]
        if '(' in token:
            temp += token.split('(')
        else:
            temp.append(token)
    temp = [token for token in temp if token != '']
    return temp


def getGlobalName(variable):
    if variable[0] == '@':
        return '_' + variable[1:]
    else:
        raise Exception("Ge moet hier nie zijn")  # pas dit zeker niet aan


# helper functie, geeft het aantal unieke waardes van een dict terug.
# Vooral gebruikt bij alloceren van nieuwe registers
def uniques(register_map: dict):
    return len(set(register_map.values()))


# convention :  $f0->$f9 = temp float registers
#               $v1 = temporary register voor int bewerkingen, bijv int direct naar stack schrijven
#               $f31 = temporary register voor float bewerkingen, bijv. float naar int converten
class Stack:
    globalTypeTable = dict()

    def __init__(self):
        self._stack = []
        self._pointers = dict()
        self.temporaries = dict()
        self.f_temporaries = dict()
        self.typeTable = dict()
        # Aantal argumenten in deze scope,
        # stel dat er registers gerefereerd worden die nooit gestored zijn, dan kunnen dit argumenten zijn
        self._arguments = 0
        self._scopes = []

    # start een nieuwe scope bij ==> hou het einde van de stack van de vorige scope bij
    def start_scope(self):
        self._scopes.append(len(self._stack))

    # eindig een scope ==> reset stack naar vorige positie
    def end_scope(self):
        last_scope = self._scopes[-1]
        retvalue = 'addu $sp, $sp, {}\n'.format(4*(len(self._stack)-last_scope))
        self._stack = self._stack[:last_scope]
        self._scopes.pop()
        return retvalue

    # allocate variable on stack
    def allocate(self, variable, type):
        self._stack.append(variable)
        self.typeTable[variable] = type

    # allocate an array on the stack
    def allocate_array(self, variable, size, type):
        for i in range(int(size)):
            self._stack.append(variable)
        self.typeTable[variable] = type

    # allocate temporary for a word
    def allocate_temp(self, variable, type):
        self.temporaries[variable] = '$t{}'.format(uniques(self.temporaries))
        self.typeTable[variable] = type

    # allocate temporary for a float
    def allocate_float_temp(self, variable, type):
        self.f_temporaries[variable] = '$f{}'.format(uniques(self.f_temporaries))
        self.typeTable[variable] = type

    # save the type of a variable
    def add_variable_type(self, variable, type):
        self.typeTable[variable] = type

    # clear all temporary variables
    def clear_temporaries(self):
        self.temporaries = {}
        self.f_temporaries = {}

    # returns the location of a llvm variable
    # returns None if the variable is not found
    def position(self, variable):
        if variable[0] == '@':  # global variable
            return variable

        if variable in self.temporaries:  # temporary word
            return self.temporaries[variable]

        elif variable in self.f_temporaries:  # temporary float
            return self.f_temporaries[variable]

        elif variable in self._stack:  # variable on stack
            return '{}($sp)'.format(4 * (1 + list(reversed(self._stack)).index(variable)))

        elif variable in self._pointers:  # pointer to variable
            pointee, offset, variable_offset = self._pointers[variable]

            if pointee[0] == '@':  # globale variabele
                return '{} + {}'.format(getGlobalName(pointee), 4*offset)
            else:  # variable on stack
                # Find occurence (offset + 1) in the stack
                return '{}($sp)'.format(4 * (1 + list(reversed(self._stack)).index(pointee) + offset) )

        elif int(variable[1:]) < self._arguments:  # function argument
            offset = (self._arguments - int(variable[1:])) * 4
            return '{}($fp)'.format(offset)

    def add_pointer(self, pointer, pointee, offset=0):  # voeg pointer toe (vooral gebruikt bij array indexing)
        if '%' in offset:
            variable_offset = [offset]
            offset = 0
        else:
            offset = int(offset)
            variable_offset = []
        while pointee not in self._stack and pointee[0] != '@':
            pointee, increase, variables = self._pointers[pointee]
            offset += increase
            variable_offset += variables

        self._pointers[pointer] = pointee, offset, variable_offset

        if pointee in Stack.globalTypeTable:
            self.typeTable[pointer] = Stack.globalTypeTable[pointee]

        if pointee in self.typeTable:
            self.typeTable[pointer] = self.typeTable[pointee]

    def store_registers(self):  # sla alle gebruikte registers op op de stack (voor functiecall)
        retvalue = ""
        i = 0
        for temp in set(self.f_temporaries.values()):
            retvalue += "swc1 {}, -{}($sp)\n".format(temp, i)
            i += 4
        for temp in set(self.temporaries.values()):
            retvalue += "sw {}, -{}($sp)\n".format(temp, i)
            i += 4
        retvalue += "subu $sp, $sp, {}\n\n".format(i)
        return retvalue

    def load_registers(self):  # laad alle gebruikte registers terug in (na functiecall)
        retValue = ""
        i = 0

        for temp in reversed(list(set(self.temporaries.values()))):
            i += 4
            retValue += "lw {}, {}($sp)\n".format(temp, i)

        for temp in reversed(list(set(self.f_temporaries.values()))):
            i += 4
            retValue += "lwc1 {}, {}($sp)\n".format(temp, i)

        retValue += "addu $sp, $sp, {}\n\n".format(i)
        return retValue

    def assign_same_temporary(self, newRegister, oldRegister):  # geef newRegister dezelfde temporary als oldRegister
        # Vooral gebruikt bij operations met een immediate
        if oldRegister in self.temporaries:
            self.temporaries[newRegister] = self.temporaries[oldRegister]
        if oldRegister in self.f_temporaries:
            self.f_temporaries[newRegister] = self.f_temporaries[oldRegister]

        self.typeTable[newRegister] = self.typeTable[oldRegister]


class LLVMTranspiler:
    def __init__(self, filename, fileLookALike=None):
        if filename[-2:0] == 'll':
            self._llvmFile = open(filename, "r")
            open(filename.split('.ll')[0] + '.asm', "w+")
        elif fileLookALike is not None:
            self._llvmFile = fileLookALike
            self._mipsFile = open(filename + '.asm', "w+")
        self._textFragment = ''
        self._dataFragment = ''
        self._positiontables = []
        self._IOdefined = False
        self._textCreated = False

    def loadFloatImmediate(self, floatregister, hexFloat):
        retvalue = 'li $v1, {}\n'.format(hexFloat)
        retvalue += 'mtc1 $v1, {}\n\n'.format(floatregister)
        return retvalue

    def createTextFragment(self):
        self._textFragment += '\n.text\n'

    def globalAssignment(self, tokens):
        global_variable = getGlobalName(tokens[0])

        if tokens[3][0] == '[':  # Array type
            Stack.globalTypeTable[tokens[0]] = tokens[5][:-1]
            if 'float' in tokens[5]:
                type = '.float'
            else:
                type = '.word'
            self._dataFragment += '{}: {} '.format(global_variable, type)
            for i in range(7, len(tokens) - 2, 2):
                value = tokens[i].split(']')[0]
                if value == 'null':
                    value = '0'
                if type == '.float':
                    value = struct.unpack('!f', bytes.fromhex(value[2:]))[0]
                if i > 7:
                    self._dataFragment += ', '
                self._dataFragment += '{}'.format(value)
            self._dataFragment += '\n'
            return

        if 'common' in tokens:  # default initialisation
            value = tokens[5]
            type = tokens[4]

        elif 'getelementptr' in tokens:
            print(tokens)
            type = 'test'
            value = 'test'

        elif 'bitcast' in tokens:  # cast pointer of pointer to other global
            value = tokens[6]
            type = tokens[8]

        else:  # normal initialisation with value
            value = tokens[4]
            type = tokens[3]

        Stack.globalTypeTable[tokens[0]] = type

        if value == 'null':
            value = '0'

        if type == 'float':
            type = '.float'
            value = str(struct.unpack('!f', bytes.fromhex(value[2:]))[0])
        else:
            type = '.word'

        if '@' in value:
            value = getGlobalName(value)
            self._dataFragment += '{}: {} 0\n'.format(global_variable, type)
            self._textFragment += 'la $v1, {}\n'.format(value)
            self._textFragment += 'sw $v1, {}\n\n'.format(global_variable)

        else:
            self._dataFragment += '{}: {} {}\n'.format(global_variable, type, value)

    def functionDefinition(self, tokens):
        # Argumenten worden opgeslagen op de stack

        self._positiontables.append(Stack())
        for i in range(len(tokens)-4):  # save argument types
            type = tokens[3+i]
            self._positiontables[-1].add_variable_type('%{}'.format(i), type)
        name = getGlobalName(tokens[2])
        self._textFragment += '\n{}:\n'.format(name)
        self._textFragment += 'sw $fp, ($sp) \nmove $fp, $sp \nsubu $sp, $sp, 8 \nsw $ra, -4($fp)\n\n'

        argumentSize = len(tokens) - 4

        # TODO: als ooit tijd : argumenten duidelijker meegeven aan extra classe
        self._positiontables[-1]._arguments = argumentSize

    def restorePtrs(self):
        self._textFragment += 'lw $ra, -4($fp) \nmove $sp, $fp \nlw $fp, ($sp)\n'
        self._textFragment += 'jr $ra\n'

    def allocate(self, tokens):
        register = tokens[0]
        type = tokens[3]
        if '[' in tokens[3]:  # array
            self._positiontables[-1].allocate_array(register, tokens[3][1:], tokens[5][:-1])
            self._textFragment += 'subu $sp, $sp, {}\n\n'.format(4 * int(tokens[3][1:]))

        else:  # Variable
            self._positiontables[-1].allocate(register, type)
            self._positiontables[-1].add_variable_type(register, type)
            self._textFragment += 'subu $sp, $sp, 4\n'

    def store(self, tokens):
        value = tokens[2]
        register = tokens[4]
        to_register = self._positiontables[-1].position(register)

        if '%' in value:  # sla temporary op op de stack of sla argumenten op op stack
            lhs_type = self._positiontables[-1].typeTable[value]
            rhs_type = self._positiontables[-1].typeTable[register]

            if lhs_type == rhs_type:
                from_register = self._positiontables[-1].position(value)

                if '$fp' in from_register:  # functie argumenten opslaan op stack in frame
                    self._textFragment += 'lw $v1, {}\n'.format(from_register)
                    self._textFragment += 'sw $v1, {}\n'.format(to_register)

                elif '$f' in from_register:  # temporary float opslaan in variabele
                    self._textFragment += 'swc1 {}, {}\n'.format(from_register, to_register)

                elif '$t' in from_register:  # temporary word opslaan in variabele
                    self._textFragment += 'sw {}, {}\n'.format(from_register, to_register)

            elif lhs_type+'*' == rhs_type:  # pak referentie van variabele
                from_register = self._positiontables[-1].position(value)
                self._textFragment += 'la $v1, {}\n'.format(from_register)
                self._textFragment += 'sw $v1, {}\n\n'.format(to_register)

        elif '@' in value:  # sla pointer naar globale variabele op
            value = getGlobalName(value)
            self._textFragment += 'la $v1, {}\n'.format(value)
            self._textFragment += 'sw $v1, {}\n'.format(to_register)

        else:  # sla immediate op op stack of in globale variabele
            lhs_type = tokens[1]
            rhs_type = self._positiontables[-1].typeTable[register]
            if '@' in to_register:
                to_register = getGlobalName(to_register)

            if lhs_type == rhs_type:
                self._textFragment += 'li $v1, {}\n'.format(value)
                self._textFragment += 'sw $v1, {}\n\n'.format(to_register)

            else:  # sla immediate op in pointer
                self._textFragment += 'li $v1, {}\n'.format(value)
                self._textFragment += 'sw $v1, ({})\n\n'.format(to_register)

        self._positiontables[-1].clear_temporaries()

    def makePointer(self, tokens):
        variables = [token for token in tokens if token[0] == '%' or token[0] == '@']
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
            var = getGlobalName(tokens[2])
            self._textFragment += 'lw $v0, {}\n'.format(var)
        else:
            value = tokens[2]
            self._textFragment += 'li $v0, {}\n'.format(value)

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
            string_position = self._positiontables[-1].position(tokens[tokens.index(identifier) + 2])
            self._textFragment += 'la $a0, {}\n'.format(string_position)
            for j in range(tokens.index(identifier) + 4, len(tokens), 2):
                parameters.append(tokens[j])
            self._textFragment += 'li $a1, {}\n'.format(len(parameters))
            identifier = identifier[1:]

        else:
            j = tokens.index(identifier) + 2
            while j < len(tokens):
                if tokens[j] == 'signext':
                    j += 1
                parameters.append(tokens[j])
                j += 2

            identifier = getGlobalName(identifier)

        self._textFragment += self._positiontables[-1].store_registers()

        for j in range(len(parameters)):  # store parameters on stack
            stack_offset = -4 * j
            parameter = parameters[j]
            if parameter[0] == '%':  # parameter is local variabele
                from_register = self._positiontables[-1].position(parameter)
                if '$f' in from_register:
                    self._textFragment += 'swc1 {}, {}($sp)\n'.format(from_register, stack_offset)

                elif '$t' in from_register:
                    self._textFragment += 'sw {}, {}($sp)\n'.format(from_register, stack_offset)

                else:  # variabele op stack
                    type = tokens[tokens.index(parameter)-1]  # hacky code, maar zou moeten werken.

                    if type != self._positiontables[-1].typeTable[parameter]:
                        self._textFragment += 'la $v1, {}\n'.format(from_register)
                    else:
                        self._textFragment += 'lw $v1, {}\n'.format(from_register)
                    self._textFragment += 'sw $v1, {}($sp)\n'.format(stack_offset)

            elif parameter[0] == '@':  # parameter is global variabele, dus pointer naar globale variabele
                parameter = getGlobalName(parameter)
                self._textFragment += 'la $v1, {}\n'.format(parameter)
                self._textFragment += 'sw $v1, {}($sp)\n'.format(stack_offset)

            else:  # parameter is een immediate
                self._textFragment += 'li $v1, {}\n'.format(parameter)
                self._textFragment += 'sw $v1, {}($sp)\n'.format(stack_offset)

        self._textFragment += 'subu $sp, $sp, {}\n'.format(4 * len(parameters))
        self._textFragment += 'jal {}\n'.format(identifier)
        self._textFragment += 'addu $sp, $sp, {}\n'.format(4 * len(parameters))

        self._textFragment += self._positiontables[-1].load_registers()

        if tokens[0] != 'call':  # save return value
            register = tokens[0]
            type = tokens[3]

            if self._positiontables[-1].position(register) is None:
                if tokens[3] == 'float':
                    self._positiontables[-1].allocate_float_temp(register, type)
                else:
                    self._positiontables[-1].allocate_temp(register, type)
            to_register = self._positiontables[-1].position(register)

            if '$f' in to_register:
                self._textFragment += 'mtc1 $v0, {}\n\n'.format(to_register)
            else:
                self._textFragment += 'move {}, $v0\n\n'.format(to_register)

    def operation(self, tokens):
        to_register = self._positiontables[-1].position(tokens[0])
        operator = tokens[2]
        type = tokens[3]
        lhs = tokens[4]
        rhs = tokens[5]

        if lhs[0] == '%':  # lhs is temporary

            if rhs[0] == '%':  # gebruik lokale variabele
                rhs = self._positiontables[-1].position(rhs)
                lhs = self._positiontables[-1].position(lhs)
                self._textFragment += '{} {}, {}, {}\n'.format(operator, to_register, lhs, rhs)

            elif rhs[0] == '@':  # gebruik globale variabele
                # Zou normaal nooit kunnen gebeuren, want globale variabele wordt ingeladen in lokale variabele bij operation
                # Wordt erin gelaten voor eventuele fouten te vinden
                print("Dit zou niet moeten gebeuren : {}".format(tokens))

            else:  # use immediate
                if to_register is None:
                    self._positiontables[-1].assign_same_temporary(tokens[0], lhs)
                    to_register = self._positiontables[-1].position(tokens[0])
                operator += 'i'
                self._textFragment += '{} {}, {}, {}\n'.format(operator, to_register, to_register, rhs)

        else:  # lhs is immediate

            if rhs[0] == '%':  # gebruik lokale variabele
                if to_register is None:
                    self._positiontables[-1].assign_same_temporary(tokens[0], rhs)
                    to_register = self._positiontables[-1].position(tokens[0])
                rhs = self._positiontables[-1].position(rhs)
                self._textFragment += 'li $v1, {}\n'.format(lhs)
                self._textFragment += '{} {}, $v1, {}\n'.format(operator, to_register, rhs)

            # rhs kan geen immediate zijn, want anders werd expressie gefold, rhs kan geen globale variabele zijn

        self._positiontables[-1].add_variable_type(tokens[0], type)

    def float_operation(self, tokens):
        to_register = self._positiontables[-1].position(tokens[0])
        operator = tokens[2][1:] + '.s'
        type = tokens[3]
        lhs = tokens[4]
        rhs = tokens[5]

        if lhs[0] == '%':  # lhs is temporary

            if rhs[0] == '%':  # gebruik lokale variabele
                rhs = self._positiontables[-1].position(rhs)
                lhs = self._positiontables[-1].position(lhs)
                self._textFragment += '{} {}, {}, {}\n'.format(operator, to_register, lhs, rhs)

            elif rhs[0] == '@':  # gebruik globale variabele
                # Zou normaal nooit kunnen gebeuren, want globale variabele wordt ingeladen in lokale variabele bij operation
                # Wordt erin gelaten voor eventuele fouten te vinden
                print("Dit zou niet moeten gebeuren : {}".format(tokens))

            else:  # use immediate
                if to_register is None:
                    self._positiontables[-1].assign_same_temporary(tokens[0], lhs)
                    to_register = self._positiontables[-1].position(tokens[0])
                self._textFragment += self.loadFloatImmediate('$f31', rhs)
                self._textFragment += '{} {}, {}, $f31\n\n'.format(operator, to_register, to_register)

        else:  # lhs is immediate

            if rhs[0] == '%':  # gebruik lokale variabele
                if to_register is None:
                    self._positiontables[-1].assign_same_temporary(tokens[0], rhs)
                    to_register = self._positiontables[-1].position(tokens[0])
                rhs = self._positiontables[-1].position(rhs)
                self._textFragment += self.loadFloatImmediate('$f31', lhs)
                self._textFragment += '{} {}, $f31, {}\n\n'.format(operator, to_register, rhs)

            # rhs kan geen immediate zijn, want dan werd expression gefold, rhs kan geen globale variabele zijn

        self._positiontables[-1].add_variable_type(tokens[0], type)

    def branch(self, tokens):
        if tokens[1] == 'label':
            if 'endif' in tokens[2]:  # end if scope
                self._textFragment += self._positiontables[-1].end_scope()
            self._textFragment += 'b {}\n\n'.format(tokens[2][1:])
        else:
            condition = tokens[2]
            cond_register = self._positiontables[-1].position(condition)
            label_true = tokens[4][1:]
            label_false = tokens[6][1:]
            self._textFragment += 'bnez {}, {}\n'.format(cond_register, label_true)

            if 'endwhile' in label_false:  # end while scope
                self._textFragment += self._positiontables[-1].end_scope()

            if 'endif' in label_true and 'else' in label_false:  # end if scope in if-else construct
                self._textFragment += self._positiontables[-1].end_scope()

            self._textFragment += 'beqz {}, {}\n\n'.format(cond_register, label_false)

    def load(self, tokens):
        if tokens[3][0] != '[':
            # TODO: is dit een fix? En waarom wordt er een load gedaan van een array vlak voor printf?
            lhs = tokens[0]
            type = tokens[3]
            rhs = tokens[5]

            self._positiontables[-1].typeTable[lhs] = type

            if self._positiontables[-1].position(lhs) is None:
                if tokens[3] == 'float':
                    self._positiontables[-1].allocate_float_temp(lhs, type)
                else:
                    self._positiontables[-1].allocate_temp(lhs, type)

            to_register = self._positiontables[-1].position(lhs)
            from_register = self._positiontables[-1].position(rhs)

            if '@' in rhs:
                from_register = getGlobalName(rhs)
                self._textFragment += 'lw {}, {}\n'.format(to_register, from_register)

            elif '$sp' in from_register:  # load variable in temporary
                if type == 'float':
                    self._textFragment += 'lwc1 {}, {}\n'.format(to_register, from_register)
                else:
                    self._textFragment += 'lw {}, {}\n'.format(to_register, from_register)

            else:  # depointer of temporary
                if type == 'float':
                    self._textFragment += 'lw $v1, ({})\n'.format(from_register)
                    self._textFragment += 'mtc1 $v1, {}\n'.format(to_register)
                else:
                    self._textFragment += 'lw {}, ({})\n'.format(to_register, from_register)

    def compare(self, tokens):
        self._positiontables[-1].allocate_temp(tokens[0], 'i1')
        to_register = self._positiontables[-1].position(tokens[0])
        comparator = tokens[3]
        lhs = tokens[5]
        rhs = tokens[6]

        # mogelijke LLVM comparators zijn slt(<), sgt(>), eq(==). mogelijke MIPS comparators zijn slt(<), sgt(), seq(==)

        if comparator == 'eq':
            comparator = 's' + comparator

        if '%' in lhs:  # lhs is temporary
            lhs = self._positiontables[-1].position(lhs)

            if rhs[0] == '%':  # compare to temporary
                rhs = self._positiontables[-1].position(rhs)

            elif comparator == 'slt':  # slt werkt niet met immediates, alle andere comparators wel, want LOGICA :(
                comparator += 'i'

            self._textFragment += '{} {}, {}, {}\n'.format(comparator, to_register, lhs, rhs)

        else:  # lhs is immediate

            if rhs[0] == '%':  # compare to temporary
                rhs = self._positiontables[-1].position(rhs)
                self._textFragment += 'li $v1, {}\n'.format(lhs)
                self._textFragment += '{} {}, $v1, {}'.format(comparator, to_register, rhs)

            # als LHS een immediate is, dan kan RHS normaal alleen een temporary zijn, want anders wordt comparison gefold

    def float_compare(self, tokens):
        self._positiontables[-1].allocate_temp(tokens[0], 'i1')
        to_register = self._positiontables[-1].position(tokens[0])
        comparator = 's' + tokens[3][1:]
        lhs = tokens[5]
        rhs = tokens[6]

        if '%' in lhs:  # lhs is temporary
            lhs = self._positiontables[-1].position(lhs)
            self._textFragment += 'mfc1 {}, {}\n'.format(to_register, lhs)

            if rhs[0] == '%':  # compare to temporary
                rhs = self._positiontables[-1].position(rhs)
                self._textFragment += 'mfc1 $v1, {}\n'.format(rhs)
                rhs = '$v1'

            else:  # compare to immediate
                if comparator == 'slt':  # slt werkt niet met immediates, alle andere comparators wel
                    comparator += 'i'

        else:  # lhs is immediate
            self._textFragment += 'li {}, {}\n'.format(to_register, lhs)

            if rhs[0] == '%':  # compare to temporary
                rhs = self._positiontables[-1].position(rhs)
                self._textFragment += 'mfc1 $v1, {}\n'.format(rhs)
                rhs = '$v1'

            # als LHS een immediate is, dan kan RHS normaal alleen een temporary zijn, want anders wordt comparison gefold

        self._textFragment += '{} {} , {}, {}\n'.format(comparator, to_register, to_register, rhs)

    def int_to_float(self, tokens):
        lhs = tokens[0]
        rhs = tokens[4]
        if lhs not in self._positiontables[-1].f_temporaries:
            self._positiontables[-1].allocate_float_temp(lhs, 'float')
        from_register = self._positiontables[-1].position(rhs)
        to_register = self._positiontables[-1].position(lhs)
        self._textFragment += 'mtc1 {}, $f31\n'.format(from_register)
        self._textFragment += 'cvt.s.w {}, $f31\n\n'.format(to_register)

    def float_to_int(self, tokens):
        lhs = tokens[0]
        rhs = tokens[4]
        if lhs not in self._positiontables[-1].temporaries:
            self._positiontables[-1].allocate_temp(lhs, 'i31')
        from_register = self._positiontables[-1].position(rhs)
        to_register = self._positiontables[-1].position(lhs)
        self._textFragment += 'cvt.w.s $f31, {}\n'.format(from_register)
        self._textFragment += 'mfc1 {}, $f31\n\n'.format(to_register)

    def bitcast(self, tokens):
        lhs = tokens[0]
        rhs = tokens[4]
        to_type = tokens[6]

        if '@' in rhs:
            self._positiontables[-1].allocate_temp(lhs, to_type)
            to_register = self._positiontables[-1].position(lhs)
            rhs = getGlobalName(rhs)
            self._textFragment += 'lw {}, {}\n'.format(to_register, rhs)
        else:
            self._positiontables[-1].assign_same_temporary(lhs, rhs)



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
            # TODO: pointers uitzoeken

            tokens = data[i]
            variables = [token for token in tokens if token[0] == '%']

            if len(tokens) == 0:
                continue

            elif tokens[0][-1] == ':':  # label
                self._textFragment += '{}\n'.format(tokens[0])
                if tokens[0].find('if') == 0 or tokens[0].find('else') == 0 or tokens[0].find('while') == 0:
                    self._positiontables[-1].start_scope()

            elif tokens[0] == 'store':  # store variable
                self.store(tokens)

            elif tokens[0] == 'ret':
                self.ret(tokens)

            elif tokens[0] == 'call':  # function call without storing return
                self.call(tokens)

            elif tokens[0] == 'br':
                self.branch(tokens)

            elif tokens[2] == 'getelementptr':
                self.makePointer(tokens)

            elif tokens[2] == 'alloca':
                self.allocate(tokens)

            elif tokens[0] == variables[0]:
                # catch all voor operaties die returnwaarde teruggeven en met up to date registers moeten werken

                # Allocate temporary for variable
                use_floats = -1

                # Aliases for llvm registers
                aliases = dict()
                if self._positiontables[-1].position(variables[0]) is None:
                    # variable heeft nog geen register ==> maak expression tree
                    expressions = []  # expressions voor in expression tree
                    for j in range(i, len(data)):
                        temp_vars = [token for token in data[j] if token[0] == '%']
                        if 'store' in data[j] or 'ret' in data[j] or 'br' in data[j]:  # expressie is hier volledig
                            break
                        elif len(temp_vars) == 3 and 'call' not in data[j]:
                            if tokens[3] == 'float' and use_floats == -1:
                                use_floats = 1
                            elif use_floats == -1:
                                use_floats = 0
                            expressions.append(data[j])
                        elif len(temp_vars) == 2 and 'load' not in data[j] and 'call' not in data[j]:
                            aliases[temp_vars[0]] = temp_vars[1]

                    if len(expressions) > 0:
                        tree = None
                        unused_expressions = [expr for expr in data[i:j] if expr not in expressions]
                        for k in range(1, len(expressions) + 1):
                            temp_tokens = expressions[-k]
                            temp_vars = [token for token in temp_tokens if token[0] == '%']

                            while temp_vars[1] in aliases:
                                temp_vars[1] = aliases[temp_vars[1]]

                            while temp_vars[2] in aliases:
                                temp_vars[2] = aliases[temp_vars[2]]

                            if tree is None:
                                tree = ExpressionTree(temp_vars[0], temp_vars[1], temp_vars[2], temp_tokens, use_floats)
                            else:

                                if not tree.addNode(temp_vars[0], temp_vars[1], temp_vars[2], temp_tokens):
                                    raise Exception("Ge moet hier nie zijn")  # pas dit zeker niet aan

                        if tree is not None:
                            tree.getErshovNumber()
                            if use_floats:
                                basenumber = uniques(self._positiontables[-1].f_temporaries)
                            else:
                                basenumber = uniques(self._positiontables[-1].temporaries)
                            register_map, new_operations = tree.getRegisters(basenumber)

                            if variables[0] in register_map:
                                # update temporaries alleen als het effect heeft op deze statement
                                if use_floats:
                                    self._positiontables[-1].f_temporaries.update(register_map)
                                else:
                                    self._positiontables[-1].temporaries.update(register_map)

                                # re-order operations
                                leftPart = data[:i]
                                rightPart = data[j:]
                                midPart = []
                                for expression in new_operations:
                                    leftPart.append(expression)
                                # insert unused expressions before the first used expression behind it
                                for expression in unused_expressions:
                                    index = data[i:j].index(expression)
                                    for k in range(i + index + 1, len(data)):
                                        if data[k] in expressions:
                                            index = leftPart.index(data[k])
                                            leftPart = leftPart[:index] + [expression] + leftPart[index:]
                                            break
                                    else:
                                        midPart.append(expression)  # behoud volgorde van ongebruikte expressies

                                data = leftPart + midPart + rightPart
                                i -= 1
                                continue

                if tokens[2] == 'add' or tokens[2] == 'sub' or tokens[2] == 'mul' or tokens[2] == 'div':
                    self.operation(tokens)

                elif tokens[2] == 'fadd' or tokens[2] == 'fsub' or tokens[2] == 'fmul' or tokens[2] == 'fdiv':
                    self.float_operation(tokens)

                elif tokens[2] == 'load':
                    self.load(tokens)

                elif tokens[2] == 'call':
                    self.call(tokens)

                elif tokens[2] == 'icmp':
                    self.compare(tokens)

                elif tokens[2] == 'fcmp':
                    self.float_compare(tokens)

                elif tokens[2] == 'fptosi':
                    self.float_to_int(tokens)

                elif tokens[2] == 'sitofp':
                    self.int_to_float(tokens)

                elif tokens[2] == 'fpext':
                    # cast float to double, wordt alleen gebruikt bij printf voor floats te printen, moet niets speciaals doen
                    # printf kan geen floats aan in LLVM, dus daarom worden dat doubles, maar MIPS printf kan wel floats aan
                    self._positiontables[-1].assign_same_temporary(variables[0], variables[1])

                elif tokens[2] == 'zext':
                    # cast bool to int, wordt alleen gebruikt bij operaties met booleans.
                    # Booleans worden als int beschouwd in MIPS, dus deze functie doet niets in MIPS
                    self._positiontables[-1].assign_same_temporary(variables[0], variables[1])

                elif tokens[2] == 'sext':
                    # cast char to int.
                    # chars worden als int beschouwd in MIPS, dus deze functie doet niets in MIPS
                    self._positiontables[-1].assign_same_temporary(variables[0], variables[1])

                elif tokens[2] == 'trunc':
                    # cast int to char.
                    # chars worden als int beschouwd in MIPS, dus deze functie doet niets in MIPS
                    self._positiontables[-1].assign_same_temporary(variables[0], variables[1])

                elif tokens[2] == 'bitcast':
                    # cast pointer to other pointer
                    self.bitcast(tokens)

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
                if not self._textCreated:
                    self._textFragment += 'jal _main\n'
                    self._textFragment += 'li $v0 10\n'  # Exit the program responsibly
                    self._textFragment += 'syscall\n'
                    self._textCreated = True

                self.functionDefinition(tokens)
                in_function = True
            elif tokens[0] == '}':
                self._positiontables.pop()

            elif tokens[0] == 'declare':
                if not self._IOdefined:
                    self._dataFragment += 'error: .asciiz "unrecognised parameter %"\n'
                self._IOdefined = True

            i += 1

        self._mipsFile.write(self._dataFragment)
        self._mipsFile.write(self._textFragment)
        if self._IOdefined:
            self._mipsFile.write(printf)
            self._mipsFile.write(scanf)
        self._mipsFile.close()
