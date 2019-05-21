class ExpressionTree:
    def __init__(self, variable, left, right, operator):
        self.var = variable
        self.ershovNumber = None
        self.register = None
        
        self.left = ExpressionTree(left, None, None, None)
        self.right = ExpressionTree(right, None, None, None)
        self.operator = operator

    def addNode(self, var, left, right, operator):
        pass

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

    def getRegisters(self, baseNumber):
        self.getErshovNumber()
        if self.left.ershovNumber == self.right.ershovNumber:
            right = self.right.getRegisters(baseNumber + 1)
            left = self.left.getRegisters(baseNumber)
        else:
            right = self.right.getRegisters(baseNumber)
            left = self.left.getRegisters(baseNumber)
        self.register = baseNumber