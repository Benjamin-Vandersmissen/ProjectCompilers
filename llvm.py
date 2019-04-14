import struct


# Change the format from a float to a hexadecimal number
def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])


# Cast the C type to the correct format for llvm and gives the align number
def checkTypeAndAlign(typename):
    align = 'ERROR'
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
    else:
        raise Exception('Unknown type found in function checkTypeAndAlign!')

    return typename, align


# Cast the C value to the correct format for llvm
def valueTransformer(typename, value):
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
            return str(float_to_hex(float(ord(value)))) + '00000000'
        elif isinstance(value, float):
            return str(float_to_hex(value)) + '00000000'


# Create the right llvm code to change a type of the value of an llvm variable and returns the llvm variable name
# expects targetType to be an llvmType
# expects varName in form of %1 or @a  (llvm)
def changeLLVMType(targetType, varName, funcDef, file):
    if varName[0] == '%':
        typeAndAlign = funcDef.typeAndAlignTable[varName[1:len(varName)]]
    elif varName[0] == '@':
        typeAndAlign = funcDef.parent.typeAndAlignTable[varName[1:len(varName)]]
    else:
        raise Exception('The given variable name "' + str(varName) + '" isn\'t an llvm variable name!')

    if targetType != typeAndAlign[0]:
        # %4 = trunc i32 %3 to i8
        operation = 'ERROR'
        if typeAndAlign[0] == 'i1':
            targetType = 'i32'
            operation = 'zext'
        elif typeAndAlign[0] == 'i32':
            if targetType == 'i8':
                operation = 'trunc'
            elif targetType == 'float':
                operation = 'sitofp'
            else:
                raise Exception('Unknown target type "' + str(typeAndAlign[0]) + '" in the function changeLLVMType!')
        elif typeAndAlign[0] == 'i8':
            if targetType == 'i32':
                operation = 'sext'
            elif targetType == 'float':
                operation = 'sitofp'
            else:
                raise Exception('Unknown target type "' + str(typeAndAlign[0]) + '" in the function changeLLVMType!')
        elif typeAndAlign[0] == 'float':
            if targetType == 'i32':
                operation = 'fptosi'
            elif targetType == 'i8':
                operation = 'fptosi'
            else:
                raise Exception('Unknown target type "' + str(typeAndAlign[0]) + '" in the function changeLLVMType!')
        else:
            raise Exception('Unknown type "' + str(typeAndAlign[0]) + '" for variable "' + str(varName) + '" in the function changeLLVMType!')

        localNumber = funcDef.getLocalNumber(checkTypeAndAlign(targetType))
        file.write('%' + str(localNumber) + ' = ' + str(operation) + ' ' + str(typeAndAlign[0]) + ' ' + str(varName) + ' to ' + str(
            targetType) + '\n')
        return '%' + str(localNumber)
    else:
        return varName


# Create the right llvm code to get the value of the searched C variable in the right llvm type and returns the llvm variable name
# expects varName to be an C varable name, better known as the identifier member
# expects wantedType to be an llvmType
def getValueOfCVariable(varName, funcDef, file):
    if varName in funcDef.counterTable:  # If the wanted variable is a local variable
        localNumber = funcDef.counterTable[varName]
        typeAndAlign = funcDef.typeAndAlignTable[str(localNumber)]
        varName = '%' + str(localNumber)
    else:  # If the wanted variable is a global variable
        typeAndAlign = funcDef.parent.typeAndAlignTable[varName]
        varName = '@' + str(varName)
    localNumber = funcDef.getLocalNumber(typeAndAlign)
    # %3 = load i32, i32* <@a/%1>, align 4
    file.write('%' + str(localNumber) + ' = load ' + str(typeAndAlign[0]) + ', ' + str(typeAndAlign[0]) + '* ' + str(varName) + ', align ' + str(typeAndAlign[1]) + '\n')
    return '%' + str(localNumber)


# Get the llvm type of a C variable
# expects varName to be an C varable name, better known as the identifier member
def getLLVMTypeOfCVariable(varName, funcDef):
    if varName in funcDef.counterTable:  # If the wanted variable is a local variable
        localNumber = funcDef.counterTable[varName]
        typeAndAlign = funcDef.typeAndAlignTable[str(localNumber)]
    else:  # If the wanted variable is a global variable
        typeAndAlign = funcDef.parent.typeAndAlignTable[varName]
    return typeAndAlign[0]


# Store the value of an llvm variable in a llvm variable representing a C variable
# expects varName to be a C variable or better known as identifier
# expects valueVar to be an llvm varibale, better know as %1 or @a
def writeLLVMStoreForCVariable(varName, valueVar, funcDef, file):
    if varName in funcDef.counterTable:  # If the wanted variable is a local variable
        localNumber = funcDef.counterTable[varName]
        typeAndAlign = funcDef.typeAndAlignTable[str(localNumber)]
        varName = '%' + str(localNumber)
    else:  # If the wanted variable is a global variable
        typeAndAlign = funcDef.parent.typeAndAlignTable[varName]
        varName = '@' + str(varName)
    changeLLVMType(typeAndAlign[0], valueVar, funcDef, file)
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
        if isinstance(cur, str):
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
        if comparison:
            cur = changeLLVMType(llvmReturnType, cur, funcDef, file)
    return cur

#  java -jar antlr-4.7.2-complete.jar -Dlanguage=Python3 smallC.g4 -visitor
