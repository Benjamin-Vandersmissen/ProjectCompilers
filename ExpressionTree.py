class ExpressionTree:
    def __init__(self, variable, left, right, operator):
        self.var = variable
        self.ershovNumber = None
        self.register = None
        
        self.left = ExpressionTree(left, None, None, None)
        self.right = ExpressionTree(right, None, None, None)
        self.operator = operator

    def addNode(self, var, left, right, operator):
        if self.left.var == var:
            self.left = ExpressionTree(var, left, right, operator)
        elif self.right.var == var:
            self.right = ExpressionTree(var, left, right, operator)
        elif self.left.addNode(var, left, right, operator):
            return True
        elif self.right.addNode(var, left, right, operator):
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
        if self.left.ershovNumber == self.right.ershovNumber:
            registerMap = self.right.getRegisters(baseNumber + 1, registerMap)
            self.register = baseNumber + self.ershovNumber
        else:
            registerMap = self.right.getRegisters(baseNumber, registerMap)
            self.register = baseNumber + self.ershovNumber - 1
        self.left.getRegisters(baseNumber, registerMap)
        registerMap[self.var] = self.register
        return registerMap