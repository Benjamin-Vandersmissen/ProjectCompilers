class ExpressionTree:
    def __init__(self, variable, left, right, parent = None):
        self.var = variable
        self.ershovNumber = None
        self.register = None

        if left is None or right is None:
            self.left = ExpressionTree(left, None, None, self)
            self.right = ExpressionTree(right, None, None, self)

    def addNode(self, var, left, right):
        if self.left is None or self.right is None:
            return False
        if self.left.var == var:
            self.left = ExpressionTree(var, left, right, self)
            return True
        elif self.right.var == var:
            self.right = ExpressionTree(var, left, right, self)
            return True
        elif self.left.addNode(var, left, right):
            return True
        elif self.right.addNode(var, left, right):
            return True
        else:
            return False

    def getErshovNumber(self):
        if self.left is None or self.right is None:
            self.ershovNumber = 1
        else :
            left = self.left.getErshovNumber()
            right = self.right.getErshovNumber()
            if left == right:
                self.ershovNumber = left
            elif left > right:
                self.ershovNumber = left
            elif left < right:
                self.ershovNumber = right
        return self.ershovNumber

    def getRegisters(self, baseNumber, registerMap = None):
        if registerMap is None:
            registerMap = dict()
        if self.left is None or self.right is None:
            return registerMap

        if self.left.ershovNumber == self.right.ershovNumber:
            if self.left.left is None or self.left.right is None:
                self.left.register = baseNumber + self.ershovNumber - 1
                registerMap[self.left.var] = self.left.register
                self.right.register = baseNumber + self.ershovNumber
                registerMap[self.right.var] = self.right.register
            else:
                registerMap = self.right.getRegisters(baseNumber + 1, registerMap)
            self.register = baseNumber + self.ershovNumber
        else: # TODO: depending which is the biggest!! TO BE FIXED
            if self.right.left is None or self.right.right is None:
                self.left.register = baseNumber + self.ershovNumber - 1  # if big
                registerMap[self.left.var] = self.left.register
                self.right.register = baseNumber + self.ershovNumber - 2  # if small
                registerMap[self.right.var] = self.right.register
            else:
                registerMap = self.right.getRegisters(baseNumber, registerMap)
            self.register = baseNumber + self.ershovNumber - 1
        self.left.getRegisters(baseNumber, registerMap)
        registerMap[self.var] = self.register
        return registerMap