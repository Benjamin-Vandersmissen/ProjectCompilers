import llvm
class LLVMTranspiler:
    def __init__(self, filename):
        self._llvmFile = open(filename, "r")
        self._mipsFile = open(filename.split('.ll')[0]+'.asm', "w+")
        self._textFragment = ''
        self._dataFragment = ''

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
        self._textFragment += 'li $v0 10\n'
        self._textFragment += 'syscall\n'

    def globalAssignment(self, line):
        global_variable, line = self.consumeUntil(line, ' = ')
        _, line = self.consumeUntil(line, 'global ')
        global_variable = self.getGlobalName(global_variable)
        type, line = self.consumeUntil(line, ' ')
        value, line = self.consumeUntil(line, ', ')
        if type == 'float':
            type = '.float'
            value = llvm.hex_to_float(value)

        else:
            type = '.word'
        self._dataFragment += '{}: {} {}\n'.format(global_variable, type, value)

    def functionDefinition(self,line):
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

            if 'call' in line: #TODO: handle calls much better
                self.functionCall(line)

        self._mipsFile.write(self._dataFragment)
        self._mipsFile.write(self._textFragment)
        self._mipsFile.close()
