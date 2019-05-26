class ExpressionTree:
    def __init__(self, variable, left, right, expression, use_float_registers=False, parent=None):
        self.var = variable
        self.ershovNumber = None
        self.register = None
        self.left = None
        self.right = None
        self.expression = expression
        self.parent = parent
        self.base = 0
        self.use_float_registers = use_float_registers

        if left is not None and right is not None:
            self.left = ExpressionTree(left, None, None, None, self.use_float_registers, self)
            self.right = ExpressionTree(right, None, None, None, self.use_float_registers, self)

    def addNode(self, var, left, right, expression):
        if self.left is None or self.right is None:
            return False
        if self.left.var == var:
            self.left = ExpressionTree(var, left, right, expression, self.use_float_registers, self)
            return True
        elif self.right.var == var:
            self.right = ExpressionTree(var, left, right, expression, self.use_float_registers, self)
            return True
        elif self.left.addNode(var, left, right, expression):
            return True
        elif self.right.addNode(var, left, right, expression):
            return True
        else:
            return False

    def getErshovNumber(self):
        if self.left is None or self.right is None:
            self.ershovNumber = 1
        else:
            left = self.left.getErshovNumber()
            right = self.right.getErshovNumber()
            if left == right:
                self.ershovNumber = left + 1
            else:
                self.ershovNumber = max(left, right)
        return self.ershovNumber

    def getRegisters(self, baseNumber):
        self.base = baseNumber
        self.register = self.ershovNumber + self.base - 1

        registerMap = dict()
        operations = []

        if self.left is None or self.right is None:
            if self.use_float_registers:
                return {self.var: '$f{}'.format(self.register)}, []
            return {self.var: '$t{}'.format(self.register)}, []

        if self.left.ershovNumber == self.right.ershovNumber:
            pair = self.right.getRegisters(baseNumber + 1)
            registerMap.update(pair[0])
            operations += pair[1]

            pair = self.left.getRegisters(baseNumber)
            registerMap.update(pair[0])
            operations += pair[1]

        elif self.left.ershovNumber < self.right.ershovNumber:
            pair = self.right.getRegisters(baseNumber)
            registerMap.update(pair[0])
            operations += pair[1]

            pair = self.left.getRegisters(baseNumber)
            registerMap.update(pair[0])
            operations += pair[1]

        elif self.left.ershovNumber > self.right.ershovNumber:
            pair = self.left.getRegisters(baseNumber)
            registerMap.update(pair[0])
            operations += pair[1]

            pair = self.right.getRegisters(baseNumber)
            registerMap.update(pair[0])
            operations += pair[1]

        if self.use_float_registers:
            registerMap[self.var] = '$f{}'.format(self.register)
        else:
            registerMap[self.var] = '$t{}'.format(self.register)
        return registerMap, operations + [self.expression]
