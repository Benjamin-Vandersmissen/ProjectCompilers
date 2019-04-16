import struct

# Class that looks like file object
class FileLookALike():
    def __init__(self):
        self.text = ''

    def write(self, text):
        self.text += text

# Change the format from a float to a hexadecimal number
def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

# Check if type is pointer, if so returns the amount of pointers
def isPointer(typename):
    if typename[-1] == '*':
        amount = 0
        for i in range(len(typename)):
            if typename[i] == '*':
                amount += 1
        return amount
    return 0

# Cast the C type to the correct format for llvm and gives the align number
def checkTypeAndAlign(typename):
    # Check if pointer if so take type and save amount of stars
    pointerAmount = isPointer(typename)
    if pointerAmount != 0:
        typename = typename[0:(-pointerAmount)]
    # Check the type
    if typename == 'int' or typename == 'i32':
        typename = 'i32'
        align = '4'
    elif typename == 'char' or typename == 'i8':
        typename = 'i8'
        align = '1'
    elif typename == 'float':
        typename = 'float'
        align = '4'
    elif typename == 'void':
        typename = 'void'
        align = 'OK'
    elif typename == 'i1':
        typename = 'i1'
        align = 'OK'
    elif typename == 'return':
        typename = 'return'
        align = 'OK'
    else:
        raise Exception('Unknown type "' + str(typename) + '"found in function checkTypeAndAlign!')
    # If a pointer add the stars to the type
    if pointerAmount != 0:
        for _ in range(pointerAmount):
            typename += '*'
        align = '8'

    return typename, align


# Cast the C value to the correct format for llvm
def valueTransformer(typename, value):  # TODO: llvm: als float al in hex staat en hierin komt, wordt het dan niet een char? werkt dit, zo niet aanpassen dat hex eerst float wordt!
    if typename == 'int' or typename == 'i32':
        if isinstance(value, int):
            return value
        elif isinstance(value, str):
            return ord(value)
        elif isinstance(value, float):
            return round(value)
    elif typename == 'char' or typename == 'i8':
        if isinstance(value, int):
            return value
        elif isinstance(value, str):
            return ord(value)
        elif isinstance(value, float):
            return int(value)
    elif typename == 'float':
        if isinstance(value, int):
            return str(float_to_hex(float(value))) + '00000000'
        elif isinstance(value, str):
            if value[0] == '0' and value[-8:len(value)] == '00000000':
                return value
            else:
                return str(float_to_hex(float(ord(value)))) + '00000000'
        elif isinstance(value, float):
            return str(float_to_hex(value)) + '00000000'
    else:
        raise Exception('Unknown typename "' + str(typename) + '" given in valueTransformer!')


# Create the right llvm code to change a type of the value of an llvm variable and returns the llvm variable name
# expects targetType to be an llvmType
# expects varName in form of %1 or @a  (llvm)
def changeLLVMType(targetType, varName, funcDef, file):  # TODO: llvm: add i64 for every type + finish if var is pointer
    if isinstance(varName, str):
        if varName[0] == '%':
            typeAndAlign = funcDef.typeAndAlignTable[varName[1:len(varName)]]
        elif varName[0] == '@':
            typeAndAlign = funcDef.parent.typeAndAlignTable[varName[1:len(varName)]]
        else:
            raise Exception('Unknown type of llvm variable: ' + str(varName))
    else:  # No variable means a value
        return valueTransformer(targetType, varName)
    # Change to type of the value to the target type
    if targetType != typeAndAlign[0]:
        varType = typeAndAlign[0]
        originalTargetType = 'ERROR'
        if isPointer(varType[0]):  # If the variable is already a pointer
            if isPointer(targetType):  # If target type is a pointer
                operation = 'bitcast'
            elif targetType == 'i64':
                operation = 'ptrtoint'
            else:
                raise Exception('Unknown target type "' + str(varType) + '" in the function changeLLVMType!')
        elif varType == 'i1':
            originalTargetType = targetType
            targetType = 'i32'
            operation = 'zext'
        elif varName == 'i64':
            if isPointer(targetType):
                operation = 'inttoptr'
        elif varType == 'i32':
            if isPointer(targetType):  # If target type is a pointer
                operation = 'bitcast'
                varType = 'i32*'
            elif targetType == 'i8':
                operation = 'trunc'
            elif targetType == 'float':
                operation = 'sitofp'
            elif targetType == 'i64':
                operation = 'sext'
            else:
                raise Exception('Unknown target type "' + str(varType) + '" in the function changeLLVMType!')
        elif varType == 'i8':
            if isPointer(targetType):
                operation = 'bitcast'
                varType = 'i8*'
            elif targetType == 'i32':
                operation = 'sext'
            elif targetType == 'float':
                operation = 'sitofp'
            else:
                raise Exception('Unknown target type "' + str(varType) + '" in the function changeLLVMType!')
        elif varType == 'float':
            if isPointer(targetType):
                operation = 'bitcast'
                varType = 'float*'
            elif targetType == 'i32':
                operation = 'fptosi'
            elif targetType == 'i8':
                operation = 'fptosi'
            else:
                raise Exception('Unknown target type "' + str(varType) + '" in the function changeLLVMType!')
        else:
            raise Exception('Unknown type "' + str(varType) + '" for variable "' + str(varName) + '" in the function changeLLVMType!')

        localNumber = funcDef.getLocalNumber(checkTypeAndAlign(targetType))
        # %4 = trunc i32 %3 to i8
        file.write('%' + str(localNumber) + ' = ' + str(operation) + ' ' + str(varType) + ' ' + str(varName) + ' to ' + str(
            targetType) + '\n')
        if varType == 'i1':
            return changeLLVMType(originalTargetType, '%' + str(localNumber), funcDef, file)
        else:
            return '%' + str(localNumber)
    else:
        return varName
        

# Create the right llvm code to get the value of the searched C or llvm variable and returns the llvm variable name
# expects varName to be an C or llvm variable name
def getValueOfVariable(varName, funcDef, codeBody, file):
    if varName[0] == '%':
        typeAndAlign = funcDef.typeAndAlignTable[varName[1:len(varName)]]
    elif varName[0] == '@':
        typeAndAlign = funcDef.parent.typeAndAlignTable[varName[1:len(varName)]]
    else:
        temp = getLLVMOfCVarible(varName, funcDef, codeBody)
        varName = temp[0]
        typeAndAlign = temp[1]
    localNumber = funcDef.getLocalNumber(typeAndAlign)
    # %3 = load i32, i32* <@a/%1>, align 4
    file.write('%' + str(localNumber) + ' = load ' + str(typeAndAlign[0]) + ', ' + str(typeAndAlign[0]) + '* ' + str(varName) + ', align ' + str(typeAndAlign[1]) + '\n')
    return '%' + str(localNumber)


# Returns the llvm variable that represents the C variable
# expects varName to be an C varable name, better known as the identifier member
def getLLVMOfCVarible(varName, funcDef, codeBody):
    if varName in codeBody.counterTable:  # If the wanted variable is a local variable
        localNumber = codeBody.counterTable[varName]
        typeAndAlign = funcDef.typeAndAlignTable[str(localNumber)]
        varName = '%' + str(localNumber)
    else:  # If the wanted variable is a global variable
        typeAndAlign = funcDef.parent.typeAndAlignTable[varName]
        varName = '@' + str(varName)
    return varName, typeAndAlign


# Get the llvm type of a C variable
# expects varName to be an C varable name, better known as the identifier member
def getLLVMTypeOfCVariable(varName, funcDef, codeBody):
    if varName in codeBody.counterTable:  # If the wanted variable is a local variable
        localNumber = codeBody.counterTable[varName]
        typeAndAlign = funcDef.typeAndAlignTable[str(localNumber)]
    else:  # If the wanted variable is a global variable
        typeAndAlign = funcDef.parent.typeAndAlignTable[varName]
    return typeAndAlign[0]


# Store the value of an llvm variable in a llvm variable representing a C variable
# expects varName to be a C variable or better known as identifier
# expects valueVar to be an llvm varibale, better know as %1 or @a
def writeLLVMStoreForCVariable(varName, valueVar, funcDef, codeBody, file):
    if varName in codeBody.counterTable:  # If the wanted variable is a local variable
        localNumber = codeBody.counterTable[varName]
        typeAndAlign = funcDef.typeAndAlignTable[str(localNumber)]
        varName = '%' + str(localNumber)
    else:  # If the wanted variable is a global variable
        typeAndAlign = funcDef.parent.typeAndAlignTable[varName]
        varName = '@' + str(varName)
    if not (isinstance(valueVar, str) and (valueVar[0] == '%' or valueVar[0] == '@')):
        valueVar = valueTransformer(typeAndAlign[0], valueVar)
    else:
        valueVar = changeLLVMType(typeAndAlign[0], valueVar, funcDef, file)
    # store i32 %2, i32* %1, align 4
    file.write('store ' + str(typeAndAlign[0]) + ' ' + str(valueVar) + ', ' + str(typeAndAlign[0]) + '* ' + str(varName) + ', align ' + str(typeAndAlign[1]) + '\n')


# Get the llvm type of an llvm variable
# expects varName to be an llvm varable name, better known as %1 or @a
def getLLVMTypeOfLLVMVariable(varName, funcDef):
    if varName[0] == '%':
        temp = varName[1:len(varName)]
        typeAndAlign = funcDef.typeAndAlignTable[temp]
    elif varName[0] == '@':
        typeAndAlign = funcDef.parent.typeAndAlignTable[varName[1:len(varName)]]
    else:
        raise Exception('The given variable name "' + str(varName) + '" isn\'t an llvm variable name!')
    return typeAndAlign[0]


# Write the llvm code to do a full operation
# expects operands to be a list of llvm variables, better know as %1 or @a
# expects compasrion to be true if it the operation is a comparsion operation
def writeLLVMOperation(llvmOperator, llvmReturnType, operands, funcDef, file, comparison=False):
    cur = operands[0]
    for i in range(1, len(operands)):
        if isinstance(cur, str) and cur[0] != '0' and cur[-8:len(cur)] != '00000000':
            temp = changeLLVMType(llvmReturnType, cur, funcDef, file)
        else:
            temp = valueTransformer(llvmReturnType, cur)
        cur = operands[i]
        if comparison:
            typeAndAlign = checkTypeAndAlign('i1')
        else:
            typeAndAlign = checkTypeAndAlign(llvmReturnType)
        localNumber = funcDef.getLocalNumber(typeAndAlign)
        file.write('%' + str(localNumber) + ' = ' + str(llvmOperator) + ' ' + str(llvmReturnType) + ' ' + str(
            temp) + ', ' + str(cur) + "\n")
        cur = '%' + str(localNumber)
    return cur

# Returns the register which has as value a bool which is the result of the comparison between the statement and 0
def writeLLVMCompareWithZero(resultLLVMVar, funcDef, file):  # TODO: llvm: compatible met constants (misschien al verkleinen in AST?)
    # if isinstance(self.children[0], ValueNode): # or child.__class__.__name__[0:8] == 'Constant':
    #     llvmTokens.append(llvm.valueTransformer(llvmReturnType, child.value))
    # else:
    #     llvmTokens.append(llvm.changeLLVMType(llvmReturnType, child.toLLVM(file, funcDef, codeBody), funcDef, file))
    typeResult = getLLVMTypeOfLLVMVariable(resultLLVMVar, funcDef)
    operator = 'ERROR'
    if typeResult == 'i32':
        operator = 'icmp ne'
    elif typeResult == 'i8':
        operator = 'icmp ne'
    elif typeResult == 'float':
        operator = 'fcmp une'
    else:
        raise Exception('Unknown type "' + str(typeResult) + '" found!')
    typeAndAlign = checkTypeAndAlign('i1')
    localNumber = funcDef.getLocalNumber(typeAndAlign)
    # %5 = icmp ne i32 %4, 0
    file.write('%' + str(localNumber) + ' = ' + str(operator) + ' ' + str(typeResult) + ' ' + str(resultLLVMVar) + ', 0\n')
    return '%' + str(localNumber)

#  java -jar antlr-4.7.2-complete.jar -Dlanguage=Python3 smallC.g4 -visitor
