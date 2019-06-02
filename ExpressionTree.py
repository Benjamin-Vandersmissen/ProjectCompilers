class ExpressionTree:
    # aliases voor het geval dat een operatie uit meerdere types variabelen bestaat die gecast worden naar andere types
    # bv :  %3 = add %1, %2  <= %3, %2, %1 zijn ints
    #       %4 = sitofp %3 <= %4 is float
    #       %6 = fadd %4, %5 <= %5, %6 zijn floats
    #
    # De expression tree moet allebei de expressies bevatten, want %6 is afhankelijk van %3, maar %6 bevat %3 niet
    # Aliases mapt dan %4 op %3, zodat de expressie van %3 toch verwerkt wordt
    aliases = dict()

    def __init__(self, variable, left, right, expression, parent=None):
        self.var = variable
        self.ershovNumber = None
        self.register = None
        self.left = None
        self.right = None
        self.expression = expression
        self.parent = parent
        self.base = 0

        if left is not None and right is not None:
            self.left = ExpressionTree(left, None, None, None, self)
            self.right = ExpressionTree(right, None, None, None, self)

    def addNode(self, var, left, right, expression):

        alias_var = var
        while alias_var in ExpressionTree.aliases:
            alias_var = ExpressionTree.aliases[alias_var]

        if self.left is None or self.right is None:
            return False
        if self.left.var == alias_var:
            self.left = ExpressionTree(var, left, right, expression, self)
            return True
        elif self.right.var == alias_var:
            self.right = ExpressionTree(var, left, right, expression, self)
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
            return {self.var: self.register}, []

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

        registerMap[self.var] = self.register
        return registerMap, operations + [self.expression]
