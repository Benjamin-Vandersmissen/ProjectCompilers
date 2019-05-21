import llvm
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
        firstPart = hexFloat[:-12]
        secondPart = '0x' + hexFloat[-12:-8]
        retvalue = 'lui {}, {}\n'.format(tempregister, firstPart)
        retvalue += 'ori {}, {}, {}\n'.format(tempregister, tempregister, secondPart)
        retvalue += 'sw {}, -4($sp)\n'.format(tempregister)
        retvalue += 'lwc1 {}, -4($sp)\n'.format(floatregister)
        return retvalue

    def createTextFragment(self):
        self._textFragment += '\n.text\n'
        self._textFragment += 'jal main\n'
        self._textFragment += 'li $v0 10\n'  # Exit the program responsibly
        self._textFragment += 'syscall\n'

    def globalAssignment(self, line):
        global_variable, line = self.consumeUntil(line, ' = ')
        _, line = self.consumeUntil(line, 'global ')
        global_variable = self.getGlobalName(global_variable)

        if line[0] == '[':  # Array type

            type, line = self.consumeUntil(line[1:], '] ')

            if 'float' in type:
                type = '.float'

            else:
                type = '.word'

            value, line = self.consumeUntil(line[1:], ']')
            print(type, value)
            value = value.split(', ')
            value = [v.split()[1] for v in value]
            self._dataFragment += '{}: {} '.format(global_variable, type)
            for v in value:
                if v != value[-1]:
                    self._dataFragment += '{}, '.format(v)
                else:
                    self._dataFragment += '{}\n'.format(v)
            return

        type, line = self.consumeUntil(line, ' ')
        value, line = self.consumeUntil(line, ', ')
        if type == 'float':
            type = '.float'
            value = llvm.hex_to_float(value)
        else:
            type = '.word'
        self._dataFragment += '{}: {} {}\n'.format(global_variable, type, value)


    def functionDefinition(self, line):

        self._positiontables.append([])

        _, line = self.consumeUntil(line, '@')
        name, line = self.consumeUntil(line, '(')
        self._textFragment += '\n{}:\n'.format(name)
        #TODO: argumenten ? Stackptr & frameptr opslaan e.d.

    def returnFunction(self, line):
        _, line = self.consumeUntil(line, 'ret ')
        type, line = self.consumeUntil(line, ' ')
        value, line = self.consumeUntil(line, '\n')

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

        # TODO:restore stackptr and frameptr
        self._textFragment += 'jr $ra\n'

    def functionCall(self, line):

        identifier, line = self.consumeUntil(line, '(')
        #store arguments & process arguments
        #TODO: alleen de juiste reigsters, als het moet
        self._textFragment += 'jal {}\n'.format(identifier)

    def operation(self, line):
        data = [line]
        while True:
            ptr = self._llvmFile.tell()
            temp_line = self._llvmFile.readline()
            if temp_line.find('ret') == -1:
                data.append(temp_line)
            else:
                self._llvmFile.seek(ptr)  # revert line
                break

            if temp_line.find('store') == 0:
                break

        for line in data:
            if ' = alloca' in line:
                self.allocate(line)

            if ' = load' in line:
                self.load(line)

            if line.find('store') == 0:
                self.store(line)

            if ' = call' in line:
                self.functionCall(line)

            if ' = getelementptr' in line:
                self.array(line)

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

    def load(self, line):
        variable, line = self.consumeUntil(line, ' = load')
        type, line = self.consumeUntil(line, ',')
        _, line = self.consumeUntil(line, type+'* ')
        value, line = self.consumeUntil(line, ',')

        if type == 'float':
            if '@' in value:  # global variable
                value = self.getGlobalName(value)
                self._textFragment += 'lwc1 $f0, {}\n'.format(value)
            elif '%' in value:  # local variable
                offset = 4*(len(self._positiontables[-1]) - self._positiontables[-1].index(value))
                self._textFragment += 'lwc1 $f0, {}($sp)\n'.format(offset)
        else:
            if '@' in value:  # global variable
                value = self.getGlobalName(value)
                self._textFragment += 'lw $t0, {}\n'.format(value)
            elif '%' in value:  # local variable
                offset = 4*(len(self._positiontables[-1]) - self._positiontables[-1].index(value))
                self._textFragment += 'lw $t0, {}($sp)\n'.format(offset)


    def store(self, line):
        type, line = self.consumeUntil(line[6:], ' ')
        value, line = self.consumeUntil(line, ', ')
        _, line = self.consumeUntil(line, '* ')
        target, line = self.consumeUntil(line, ', ')
        offset = 4 * (len(self._positiontables[-1]) - self._positiontables[-1].index(target))
        if type == 'float':
            if '%' not in value:  # load float in normal register
                firstPart = value[:-12]
                secondPart = '0x' + value[-12:-8]
                self._textFragment += 'lui $t0, {}\n'.format(firstPart)
                self._textFragment += 'ori $t0, $t0, {}\n'.format(secondPart)
                self._textFragment += 'sw $t0, {}($sp)\n\n'.format(offset)
            else:
                self._textFragment += 'lwc1 %f0, {}($sp)\n\n'.format(offset)

        else:
            if '%' not in value:
                self._textFragment += 'li $t0, {}\n'.format(value)
            self._textFragment += 'sw $t0, {}($sp)\n\n'.format(offset)

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

    def transpile(self):
        self.createTextFragment()
        self._dataFragment += '.data\n'
        while True:
            line = self._llvmFile.readline()
            if line == '':
                break
            if line[0] == '@':
                # globale variable assignment
                self.globalAssignment(line)
            if line.find('define') == 0:
                # function definition
                self.functionDefinition(line)

            if line.find('ret') == 0:
                self.returnFunction(line)

            # if 'call' in line:  # TODO: handle calls much better
            #     self.functionCall(line)

            if line[0] == '%':
                self.operation(line)

            if line[0] == '}':
                self._positiontables.pop()

        self._mipsFile.write(self._dataFragment)
        self._mipsFile.write(self._textFragment)
        self._mipsFile.close()
