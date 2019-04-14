import struct


# Change the format from a float to a hexadecimal number
def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])


# Cast the C type to the correct format for llvm and gives the align number
def checkTypeAndAlign(typename):
    align = "ERROR"
    if typename == "int":
        typename = "i32"
        align = "4"
    elif typename == "char":
        typename = "i8"
        align = "1"
    elif typename == "float":
        typename = "float"
        align = "4"
    elif typename == "void":
        typename = "void"

    return typename, align


# Cast the C value to the correct format for llvm
def valueTransformer(typename, value):
    if typename == "int":
        if isinstance(value, int):
            return value
        elif isinstance(value, str):
            return ord(value)
        elif isinstance(value, float):
            return round(value)
    elif typename == "char":
        if isinstance(value, int):
            return value
        elif isinstance(value, str):
            return ord(value)
        elif isinstance(value, float):
            return int(value)
    elif typename == "float":
        if isinstance(value, int):
            return str(float_to_hex(float(value))) + "00000000"
        elif isinstance(value, str):
            return str(float_to_hex(float(ord(value)))) + "00000000"
        elif isinstance(value, float):
            return str(float_to_hex(value)) + "00000000"


# Create the right llvm code to change a type of the value of an llvm variable and returns the llvm variable name
# expects targetType to be an llvmType
# expects varName in form of %1 or @a  (llvm)
def changeType(targetType, varName, funcDef, file):
    if varName[0] == '%':
        typeAndAlign = funcDef.typeAndAlignTable[varName[1:len(varName)]]
    elif varName[0] == '@':
        typeAndAlign = funcDef.parent.typeAndAlignTable[varName[1:len(varName)]]
    else:
        raise Exception('The given variable name "' + str(varName) + '" isn\'t an llvm variable name!')

    if targetType != typeAndAlign[0]:
        # %4 = trunc i32 %3 to i8
        localNumber = funcDef.getLocalNumber()
        file.write("%" + str(localNumber) + " = trunc " + str(typeAndAlign[0]) + str(varName) + " to " + str(
            targetType) + "\n")
        return "%" + str(localNumber)
    else:
        return varName


# Create the right llvm code to get the value of the searched C variable in the right llvm type and returns the llvm variable name
# expects varName to be an C varable name, better know as the identifier member
# expects wantedType to be an llvmType
def getValueOfCVariable(varName, funcDef, file):
    localNumber = funcDef.getLocalNumber()
    if varName in funcDef.counterTable:  # If the wanted variable is a local variable
        varName = funcDef.counterTable[varName]
        typeAndAlign = funcDef.typeAndAlignTable[varName]
        sign = '%'
    else:  # If the wanted variable is a global variable
        typeAndAlign = funcDef.parent.typeAndAlignTable[varName]
        sign = '@'
    # %3 = load i32, i32* <@a/%1>, align 4
    file.write("%" + str(localNumber) + " = load " + str(typeAndAlign[0]) + ", " + str(typeAndAlign[0]) + "* " + str(
        sign) + str(varName) + ", align " + str(typeAndAlign[1]) + "\n")
    return "%" + str(localNumber)

#  java -jar antlr-4.7.2-complete.jar -Dlanguage=Python3 smallC.g4 -visitor
