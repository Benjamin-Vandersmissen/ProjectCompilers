import struct
import TreeNodes

# Class that looks like file object
class FileLookALike():
    def __init__(self):
        self.text = ''

    def write(self, text):
        self.text += text


# Change the format from a float to a hexadecimal number
def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])


# Change the format of a hexadecimal number to a float
def hex_to_float(h):
    return  struct.unpack('!f', bytes.fromhex(h[-16:-8]))[0]


# Check if type is pointer, if so returns the amount of pointers
def isPointer(typename):
    if typename[-1] == '*':
        amount = 0
        for i in range(len(typename)):
            if typename[i] == '*':
                amount += 1
        return amount
    return 0


# Get all information about an array type or False when it isn't an array
def getArrayTypeInfo(arrayType):
    # Check if array
    if arrayType[0] == '[' and arrayType[-1] == ']':
        for i in range(len(arrayType)):
            if arrayType[i] == ' ':
                return int(arrayType[1:i]), arrayType[i+3:-1]
    return False


# Cast the C type to the correct format for llvm and gives the align number
def checkTypeAndAlign(typename):
    # If pointer, take type and save amount of stars
    pointerAmount = isPointer(typename)
    if pointerAmount != 0:
        typename = typename[0:(-pointerAmount)]
    # If array, get all info and change typename
    arrayTypeInfo = getArrayTypeInfo(typename)
    if arrayTypeInfo:
        typename = arrayTypeInfo[1]
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
    elif typename == 'i64':
        typename = 'i64'
        align = '8'
    else:
        raise Exception('Unknown type "' + str(typename) + '" found in function checkTypeAndAlign!')
    # If array, create the right type
    if arrayTypeInfo:
        typename = '[' + str(arrayTypeInfo[0]) + ' x ' + str(typename) + ']'
    # If pointer, add the stars to the type
    if pointerAmount != 0:
        for _ in range(pointerAmount):
            typename += '*'
        align = '8'

    return typename, align


# Cast the C value to the correct format for llvm
def valueTransformer(typename, value):
    if isinstance(value, str) and value[-8:len(value)] == '00000000':
        value = hex_to_float(value)
    if typename == 'int' or typename == 'i32' or typename == 'i64':
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


# Create the right llvm code to change a type of the value (of an llvm variable) and returns the llvm variable name
# expects targetType to be an llvmType
# expects varName in form of %1 or @a  (llvm)
def changeLLVMType(targetType, varName, funcDef, file, dereference=False):
    targetType = checkTypeAndAlign(targetType)[0]
    isFloat = False
    if isinstance(varName, str) and len(varName) == 18 and varName[-8:18] == '00000000':
        isFloat = True
    if isinstance(varName, str) and not isFloat:
        if varName[0] == '%':
            typeAndAlign = funcDef.typeAndAlignTable[varName[1:len(varName)]]
        elif varName[0] == '@':
            typeAndAlign = funcDef.parent.typeAndAlignTable[varName[1:len(varName)]]
        else:
            raise Exception('Unknown type of llvm variable: ' + str(varName))
    else:  # No variable means a value
        return valueTransformer(targetType, varName)
    if targetType != typeAndAlign[0]:
        varType = typeAndAlign[0]
        operation = 'ERROR'
        originalTargetType = 'ERROR'
        if isPointer(varType):  # If the variable is already a pointer
            if isPointer(targetType):  # If target type is a pointer
                operation = 'bitcast'
            elif targetType == 'i64':
                operation = 'ptrtoint'
            else:
                raise Exception('Unknown target type "' + str(varType) + '" in the function changeLLVMType!')
        elif varType == 'i1':
            if targetType == 'i32':
                operation = 'zext'
            else:
                varName = changeLLVMType('i32', varName, funcDef, file)
                return changeLLVMType(targetType, varName, funcDef, file)
        elif varType == 'i64':
            if isPointer(targetType):
                operation = 'inttoptr'
        elif varType == 'i32':
            if isPointer(targetType):  # If target type is a pointer
                if dereference:
                    operation = 'bitcast'
                    varType = 'i32*'
                else:
                    varName = changeLLVMType('i64', varName, funcDef, file)
                    return changeLLVMType(targetType, varName, funcDef, file)
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
                if dereference:
                    operation = 'bitcast'
                    varType = 'i8*'
                else:
                    varName = changeLLVMType('i64', varName, funcDef, file)
                    return changeLLVMType(targetType, varName, funcDef, file)
            elif targetType == 'i32':
                operation = 'sext'
            elif targetType == 'float':
                operation = 'sitofp'
            elif targetType == 'i64':
                varName = changeLLVMType('i32', varName, funcDef, file)
                return  changeLLVMType(targetType, varName, funcDef, file)
            else:
                raise Exception('Unknown target type "' + str(varType) + '" in the function changeLLVMType!')
        elif varType == 'float':
            if isPointer(targetType):
                if dereference:
                    operation = 'bitcast'
                    varType = 'float*'
                else:
                    varName = changeLLVMType('i64', varName, funcDef, file)
                    return changeLLVMType(targetType, varName, funcDef, file)
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
        return '%' + str(localNumber)
    else:
        return varName
        

# Create the right llvm code to get the value of the searched C or llvm variable and returns the llvm variable name
# expects varName to be an C or llvm variable name
def getValueOfVariable(varName, funcDef, codeBody, file, depointer=False):
    if varName[0] == '%':
        typeAndAlign = funcDef.typeAndAlignTable[varName[1:len(varName)]]
    elif varName[0] == '@':
        typeAndAlign = funcDef.parent.typeAndAlignTable[varName[1:len(varName)]]
    else:
        temp = getLLVMOfCVarible(varName, funcDef, codeBody)
        varName = temp[0]
        typeAndAlign = temp[1]
    if depointer:  # The pointer (var) is loaded, but the var is of the type of the pointer
        localNumber = funcDef.getLocalNumber(checkTypeAndAlign(typeAndAlign[0][0:-1]))
    else:
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


# Get the llvm type of a variable
# Expects noC to be a bool, true if the variables can't be C variables, so they will be values
def getLLVMTypeOfVariable(varName, funcDef, codeBody):
    if isinstance(varName, str):
        if varName[0] == '%':
            typeAndAlign = funcDef.typeAndAlignTable[varName[1:len(varName)]]
        elif varName[0] == '@':
            typeAndAlign = funcDef.parent.typeAndAlignTable[varName[1:len(varName)]]
        else:
            temp = getLLVMOfCVarible(varName, funcDef, codeBody)
            varName = temp[0]
            typeAndAlign = temp[1]
    else:
        raise Exception('Unknown variable "' + str(varName) + '" found!')
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
    valueVar = changeLLVMType(typeAndAlign[0], valueVar, funcDef, file)
    # store i32 %2, i32* %1, align 4
    file.write('store ' + str(typeAndAlign[0]) + ' ' + str(valueVar) + ', ' + str(typeAndAlign[0]) + '* ' + str(varName) + ', align ' + str(typeAndAlign[1]) + '\n')


# Write the llvm code to do a full operation
# expects operands to be a list of llvm variables, better know as %1 or @a
# expects compasrion to be true if it the operation is a comparsion operation
def writeLLVMOperation(operator, operands, funcDef, codeBody, file):
    cur = operands[0]
    type1 = ''
    if isinstance(cur, TreeNodes.ValueNode):
        type1 = checkTypeAndAlign(cur.type())[0]
        cur = cur.toLLVM(file, funcDef, codeBody)
    else:
        cur = cur.toLLVM(file, funcDef, codeBody)
        type1 = getLLVMTypeOfVariable(cur, funcDef, codeBody)
    for i in range(1, len(operands)):
        temp = cur
        cur = operands[i]
        if isinstance(cur, TreeNodes.ValueNode):
            type2 = checkTypeAndAlign(cur.type())[0]
            cur = cur.toLLVM(file, funcDef, codeBody)
        else:
            cur = cur.toLLVM(file, funcDef, codeBody)
            type2 = getLLVMTypeOfVariable(cur, funcDef, codeBody)
        operationInfo = getLLVMOperatorAndReturnType(operator, type1, type2)
        temp = changeLLVMType(operationInfo[1], temp, funcDef, file)
        cur = changeLLVMType(operationInfo[2], cur, funcDef, file)
        localNumber = 'ERROR'
        if operationInfo[5]:  # If switched
            var1 = cur
            var2 = temp
        else:
            var1 = temp
            var2 = cur
        if operationInfo[4] == 1:
            typeAndAlign = checkTypeAndAlign(operationInfo[3])
            localNumber = funcDef.getLocalNumber(typeAndAlign)
            # %8 = icmp eq i8* %2, %7
            file.write('%' + str(localNumber) + ' = ' + str(operationInfo[0]) + ' ' + str(typeAndAlign[0]) + ' ' + str(
                var1) + ', ' + str(var2) + "\n")
            type1 = operationInfo[3]
        elif operationInfo[4] == 2:
            typeAndAlign = checkTypeAndAlign(operationInfo[3])
            localNumber = funcDef.getLocalNumber(typeAndAlign)
            # %9 = getelementptr inbounds i32*, i32** %4, i64 %8
            file.write('%' + str(localNumber) + ' = ' + str(operationInfo[0]) + ' ' + str(operationInfo[1][0:-1]) + ', ' + str(operationInfo[1]) + ' ' + str(var1) + ', ' + str(operationInfo[2]) + ' ' + str(var2) + '\n')
            type1 = operationInfo[3]
        elif operationInfo[4] == 3:
            localNumber = funcDef.getLocalNumber(checkTypeAndAlign('i64'))
            # %6 = sub i64 0, %5
            file.write('%' + str(localNumber) + ' = sub i64 0, ' + str(var2) + '\n')
            var2 = '%' + str(localNumber)

            typeAndAlign = checkTypeAndAlign(operationInfo[3])
            localNumber = funcDef.getLocalNumber(typeAndAlign)
            # %7 = getelementptr inbounds i32, i32* %1, i64 %6
            file.write(
                '%' + str(localNumber) + ' = ' + str(operationInfo[0]) + ' ' + str(operationInfo[1][0:-1]) + ', ' + str(
                    operationInfo[1]) + ' ' + str(var1) + ', ' + str(operationInfo[2]) + ' ' + str(var2) + '\n')
            type1 = operationInfo[3]
        cur = '%' + str(localNumber)
    return cur


def getLLVMOperatorAndReturnType(operator, type1, type2):
    operationType = 'ERROR'
    returnType = 'ERROR'
    switched = False

    if isPointer(type1) or isPointer(type2):
        switched = False
        if not isPointer(type1):
            temp = type1
            type1 = type2
            type2 = temp
            switched = True
        if isPointer(type2):
            returnType = type1
            operationType = 1
            if operator == '-':
                type1 = 'i64'
                type2 = 'i64'
                operator = 'sub'  # nsw
                returnType = 'i64'
            elif operator == '==':
                operator = 'icmp eq'
            elif operator == '<':
                operator = 'icmp ult'
            elif operator == '>':
                operator = 'icmp ugt'
            else:
                raise Exception('Operator not supported with pointer variables!')
        elif type2 == 'i64' or type2 == 'i32' or type2 == 'i8':
            type2 = type1
            operationType = 1
            returnType = type1
            if operator == '+':
                type2 = 'i64'
                operator = 'getelementptr inbounds'
                operationType = 2
                returnType = type1
            elif operator == '-':
                type2 = 'i64'
                operator = 'getelementptr inbounds'
                operationType = 3
                returnType = type1
            elif operator == '==':
                operator = 'icmp eq'
            elif operator == '<':
                operator = 'icmp ult'
            elif operator == '>':
                operator = 'icmp ugt'
            else:
                raise Exception('Unknown operator found!')
        else:
            raise Exception('No operation with a pointer and ' + str(type2) + ' exists!')
    elif type1 == 'i32':
        type2 = 'i32'
        returnType = 'i32'
    elif type1 == 'i8':
        type1 = 'i32'
        type2 = 'i32'
        returnType = 'i32'
    elif type1 == 'float':
        type2 = 'float'
        returnType = 'float'
    elif type1 == 'i1':
        if type2 == 'i1':
            type1 = 'i32'
            type2 = 'i32'
            returnType = 'i32'
        else:
            type1 = type2
            returnType = type2
    else:
        raise Exception('Unknown type "' + str(type1) + '" found!')

    if returnType == 'i32':
        if operator == '+':
            operator = 'add'  #nsw
        elif operator == '-':
            operator = 'sub'  #nsw
        elif operator == '*':
            operator = 'mul'  #nsw
        elif operator == '/':
            operator = 'sdiv'
        elif operator == '==':
            operator = 'icmp eq'
        elif operator == '<':
            operator = 'icmp slt'
        elif operator == '>':
            operator = 'icmp sgt'
        else:
            raise Exception('Unknown operator found!')
        operationType = 1

    elif returnType == 'float':
        if operator == '+':
            operator = 'fadd'
        elif operator == '-':
            operator = 'fsub'
        elif operator == '*':
            operator = 'fmul'
        elif operator == '/':
            operator = 'fdiv'
        elif operator == '==':
            operator = 'fcmp oeq'
        elif operator == '<':
            operator = 'fcmp olt'
        elif operator == '>':
            operator = 'fcmp ogt'
        else:
            raise Exception('Unknown operator found!')
        operationType = 1

    return operator, type1, type2, returnType, operationType, switched

# Returns the register which has as value a bool which is the result of the comparison between the statement and 0
def writeLLVMCompareWithZero(resultLLVMVar, funcDef, codeBody, file):  # TODO: llvm: compatible met constants (misschien al verkleinen in AST?)
    # if isinstance(self.children[0], ValueNode): # or child.__class__.__name__[0:8] == 'Constant':
    #     llvmTokens.append(llvm.valueTransformer(llvmReturnType, child.value))
    # else:
    #     llvmTokens.append(llvm.changeLLVMType(llvmReturnType, child.toLLVM(file, funcDef, codeBody), funcDef, file))
    typeResult = getLLVMTypeOfVariable(resultLLVMVar, funcDef, codeBody)
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
