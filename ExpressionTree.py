class ExpressionTree:
    def __init__(self, variable, left, right, operation, parent = None):
        self.var = variable
        self.ershovNumber = None
        self.register = None
        self.left = None
        self.right = None
        self.operation = operation
        self.parent = parent
        self.base = 0

        if left is not None and right is not None:
            self.left = ExpressionTree(left, None, None, None, self)
            self.right = ExpressionTree(right, None, None, None, self)

    def addNode(self, var, left, right, operation):
        if self.left is None or self.right is None:
            return False
        if self.left.var == var:
            self.left = ExpressionTree(var, left, right, operation, self)
            return True
        elif self.right.var == var:
            self.right = ExpressionTree(var, left, right, operation, self)
            return True
        elif self.left.addNode(var, left, right, operation):
            return True
        elif self.right.addNode(var, left, right, operation):
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
            return {self.var: self.register}, []

        if self.left.ershovNumber == self.right.ershovNumber:
            pair = self.right.getRegisters(baseNumber + 1)
            registerMap.update(pair[0])
            operations += pair[1]

            pair = self.left.getRegisters(baseNumber)
            registerMap.update(pair[0])
            operations += pair[1]
            print("{}({}) = {}({}) op {}({})".format(self.register, self.var, self.left.register, self.left.var, self.right.register, self.right.var))

        elif self.left.ershovNumber < self.right.ershovNumber:
            pair = self.right.getRegisters(baseNumber)
            registerMap.update(pair[0])
            operations += pair[1]

            pair = self.left.getRegisters(baseNumber)
            registerMap.update(pair[0])
            operations += pair[1]
            print("{}({}) = {}({}) op {}({})".format(self.register, self.var, self.left.register, self.left.var, self.right.register, self.right.var))

        elif self.left.ershovNumber > self.right.ershovNumber:
            pair = self.right.getRegisters(baseNumber + 1)
            registerMap.update(pair[0])
            operations += pair[1]

            pair = self.left.getRegisters(baseNumber)
            registerMap.update(pair[0])
            operations += pair[1]
            print("{}({}) = {}({}) op {}({})".format(self.register, self.var, self.left.register, self.left.var, self.right.register, self.right.var))

        registerMap[self.var] = self.register
        return registerMap, operations + ["{} = {} {} {}".format(self.var, self.operation, self.left.var, self.right.var)]