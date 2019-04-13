from decimal import Decimal

# Cast the type to the correct format for llvm and the align number
def checkTypeAndAlign(typename):
    if typename == "int":
        typename = "i32"
        align = "4"
    elif typename == "char":
        typename = "i8"
        align = "1"
    elif typename == "float":
        typename = "float"
        align = "4"

    return typename, align

# Cast the value to the correct format for llvm
def valueTransformer(typename, value):
    if typename == "int":
        if isinstance(value, int):
            return value
        elif isinstance(value, str):
            return ord(value)
        elif isinstance(value, float):
            return int(value)
    elif typename == "char":
        if isinstance(value, int):
            return value
        elif isinstance(value, str):
            return ord(value)
        elif isinstance(value, float):
            return int(value)
    elif typename == "float":
        if isinstance(value, int):
            return '%.2e' % Decimal(float(value))
        elif isinstance(value, str):
            return '%.2e' % Decimal(float(ord(value)))
        elif isinstance(value, float):
            return '%.2e' % Decimal(value)