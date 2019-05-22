import llvm
from ExpressionTree import *
import copy


def extractVars(line):
    vars = []
    while line.find('%') != -1:
        var = line[line.find('%'):].split()[0].split(',')[0]
        vars.append(var)
        line = line[1 + line.find('%'):]
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
    return temp


class LLVMTranspiler:
    def __init__(self, filename):
        self._llvmFile = open(filename, "r")
        self._mipsFile = open(filename.split('.ll')[0]+'.asm', "w+")
        self._textFragment = ''
        self._dataFragment = ''
        self._positiontables = []

    def consumeUntil(self, line, tokens):
        retvalue, line = line.split(tokens, 1)
        return retvalue, line

    def getGlobalName(self, variable):
        if variable[0] == '@':
            return '_' + variable[1:]
        else:
            raise Exception("Ge moet hier nie zijn") #TODO: pas dit zeker niet aan

    def loadFloatImmediate(self, tempregister, floatregister, hexFloat):
        float = hexFloat[:-8]
        retvalue = 'li {}, {}\n'.format(tempregister, float)
        retvalue += 'sw {}, -4($sp)\n'.format(tempregister)
        retvalue += 'lwc1 {}, -4($sp)\n'.format(floatregister)
        return retvalue

    def createTextFragment(self):
        self._textFragment += '\n.text\n'
        self._textFragment += 'jal main\n'
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
            for i in range(7, len(tokens)-2, 2):
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

        self._positiontables.append([])
        name = tokens[2][1:]
        self._textFragment += '\n{}:\n'.format(name)
        self._textFragment += 'sw $fp, ($sp) \nmove $fp, $sp \nsubu $sp, $sp, 8 \nsw $ra, -4($fp)\n'
        #TODO: argumenten opslaan e.d.

    def restorePtrs(self):
        self._textFragment += 'lw $ra, -4($fp) \nmove $sp, $fp \nlw $fp, ($sp)\n'
        self._textFragment += 'jr $ra\n'

    def returnFunction(self, tokens):
        type = tokens[1]
        if type == 'void':
            self.restorePtrs()
            return

        value = tokens[2]

        if type == 'float':
            # store return value in f31
            if value[0] == '%':
                # Load register
                pass
            else:
                # Load float in registers via fancy trick
                self._textFragment += self.loadFloatImmediate('$t0', '$f31', value)
            pass
        else:
            # store return value in v0
            if value[0] == '%':
                # Load register
                pass
            else:
                # Load immediate
                self._textFragment += 'li $v0, {}\n'.format(value)
            pass

        self.restorePtrs()

    def functionCall(self, line):

        pass
        # reg, line = self.consumeUntil(line, ' = call ')
        # retType, line = self.consumeUntil(line, ' @')
        # identifier, line = self.consumeUntil(line, '(')
        # #store arguments & process arguments
        # #TODO: alleen de juiste reigsters, als het moet
        # self._textFragment += 'jal {}\n'.format(identifier)

    def operation(self, index, lines):
        data = []
        for i in range(index, len(lines)):
            temp_line = lines[i]
            if temp_line.find('ret') == -1:
                data.append(temp_line)
            else:
                index = i-1
                break

            if temp_line.find('store') == 0:
                index = i
                break

        tree = None

        for line in reversed(data[1:-1]):
            tokens = tokenise(line)
            vars = [token for token in tokens if token[0] == '%']
            if len(vars) < 3:
                # bouw expression tree alleen op met expressions die 2 variables gebruiken en opslaan in een derde
                continue
            if tree is None:
                tree = ExpressionTree(vars[0], vars[1], vars[2], tokens[2])
            else:
                if not tree.addNode(vars[0], vars[1], vars[2], tokens[2]):
                    raise Exception("Ge moet hier nie zijn")  # TODO: pas dit zeker niet aan

        register_map = dict()
        new_operations = []
        if tree is not None:
            tree.getErshovNumber()
            register_map, new_operations = tree.getRegisters(0)

        for line in data:
            tokens = tokenise(line)
            vars = [token for token in tokens if token[0] == '%']
            if len(register_map) == 0:
                if tokens[2] == 'alloca':
                    self.allocate(line)

                if tokens[2] == 'load':
                    self.load(tokens, '$t0')

                if tokens[0] == 'store':
                    self.store(tokens, '$t0')

                if tokens[2] == 'call':
                    self.functionCall(line)

                if tokens[2] == 'getelementptr':
                    self.array(line)
            else:
                if tokens[2] == 'alloca':
                    self.allocate(line)

                if tokens[2] == 'load':
                    self.load(tokens, '$t0')

                if tokens[0] == 'store':
                    self.store(tokens, '$t0')

                if tokens[2] == 'call':
                    self.functionCall(line)

                if tokens[2] == 'getelementptr':
                    self.array(line)

        return index

    def allocate(self, line):
        variable, line = self.consumeUntil(line, ' = alloca ')
        type, line = self.consumeUntil(line, ',')
        if '[' in type:  # allocate array
            array_size = int(type[1:].split(' x')[0])
            for i in range(array_size):
                self._positiontables[-1].append(variable)
            self._textFragment += 'subu $sp, $sp, {}\n'.format(4*array_size)
        else:
            self._positiontables[-1].append(variable)
            self._textFragment += 'subu $sp, $sp, 4\n'

    def load(self, tokens, register):
        type = tokens[2]
        value = tokens[5]

        if type == 'float':
            if value[0] == '@':  # global variable
                value = self.getGlobalName(value)
                self._textFragment += 'lwc1 $f0, {}\n'.format(value)
            elif value[0] == '%':  # local variable
                offset = 4*(len(self._positiontables[-1]) - self._positiontables[-1].index(value))
                self._textFragment += 'lwc1 $f0, {}($sp)\n'.format(offset)
        else:
            if value[0] == '@':  # global variable
                value = self.getGlobalName(value)
                self._textFragment += 'lw {}, {}\n'.format(register, value)
            elif value[0] == '%':  # local variable
                offset = 4*(len(self._positiontables[-1]) - self._positiontables[-1].index(value))
                self._textFragment += 'lw {}, {}($sp)\n'.format(register, offset)

    def store(self, tokens, register):
        a = 0
        type = tokens[1]
        value = tokens[2]
        target = tokens[4]
        offset = 4 * (len(self._positiontables[-1]) - self._positiontables[-1].index(target))
        if type == 'float':
            if '%' not in value:  # load float in normal register
                float = value[:-18]
                self._textFragment += 'li {}, {}\n'.format(register, float)
                self._textFragment += 'sw {}, {}($sp)\n\n'.format(register, offset)
            else:
                self._textFragment += 'lwc1 $f0, {}($sp)\n\n'.format(offset)

        else:
            if '%' not in value:
                self._textFragment += 'li {}, {}\n'.format(register, value)
            self._textFragment += 'sw {}, {}($sp)\n\n'.format(register, offset)

    def array(self, line):
        variable, line = self.consumeUntil(line, ' = getelementptr inbounds')
        type, line = self.consumeUntil(line, ', ')
        _, line = self.consumeUntil(line, '* ')
        register, line = self.consumeUntil(line, ', ')
        _, line = self.consumeUntil(line, ' ')
        offset, line = self.consumeUntil(line, ', ')
        print(variable, type, register)

    def convertTo32bitFloat(self, value):
        # value is in string representation
        value = value[:-8]
        return value

    def replaceRegisters(self, startIndex, lines):
        registerLink = dict()
        i = startIndex
        while i < len(lines):
            line = lines[i]
            tokens = line.split(' ')
            if ' = load' in line:
                registerLink[tokens[0]] = tokens[5][:-1]
                del lines[i]
                continue
            elif '}' == line:
                return
            else:
                for j in range(len(tokens)):
                    if tokens[j].split(',')[0] in registerLink:
                        lines[i] = lines[i].replace(tokens[j].split(',')[0], registerLink[tokens[j].split(',')[0]])
                i += 1

    def transpile(self):
        self.createTextFragment()
        self._dataFragment += '.data\n'

        lines = self._llvmFile.read().split('\n')
        i = 0
        while i < len(lines):
            line = lines[i]
            tokens = tokenise(line)
            if len(tokens) == 0:
                i += 1
                continue
            if tokens[0][0] == '@':
                # globale variable assignment
                self.globalAssignment(tokens)
            if tokens[0] == 'define':
                # function definition
                self.functionDefinition(tokens)
                # self.replaceRegisters(i, lines)

            if tokens[0] == 'ret':
                self.returnFunction(tokens)

            # if 'call' in line:  # TODO: handle calls much better
            #     self.functionCall(line)

            if tokens[0][0] == '%':
                i = self.operation(i, lines)

            if line[0] == '}':
                self._positiontables.pop()

            i += 1

        self._mipsFile.write(self._dataFragment)
        self._mipsFile.write(self._textFragment)
        self._mipsFile.close()
