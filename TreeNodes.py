class TreeNode:
    def __init__(self):
        self.parent = None
        self.children = []

    def add(self, treenode):
        self.children.append(treenode)
        self.children[-1].parent = self

    def text(self):
        string = str()
        for child in self.children:
            string += child.text()
        return string

class ProgramNode(TreeNode):
    pass

class CodeBodyNode(TreeNode):
    pass

class StatementNode(TreeNode):
    pass

class IfBlockNode(TreeNode):
    pass

class ElseBlockNode(TreeNode):
    pass

class IfStatementNode(TreeNode):
    pass

class WhileStatementNode(TreeNode):
    pass

class WhileBlockNode(TreeNode):
    pass

class TypeNameNode(TreeNode):
    pass

class DeclarationNode(TreeNode):
    pass

class ConstantDeclarationNode(TreeNode):
    pass

class ConstantArrayListNode(TreeNode):
    pass

class ConstantAssignmentNode(TreeNode):
    pass

class ConstantExpressionNode(TreeNode):
    pass

class ConstantSumNode(TreeNode):
    pass

class ConstantProductNode(TreeNode):
    pass

class ConstantNode(TreeNode):
    pass

class ArrayListNode(TreeNode):
    pass

class FunctionDeclarationNode(TreeNode):
    pass

class ArgumentDeclarationListNode(TreeNode):
    pass

class FunctionDefinitionNode(TreeNode):
    pass

class ReturnTypeNode(TreeNode):
    pass

class ArrayElementNode(TreeNode):
    pass

class AssignmentNode(TreeNode):
    pass

class IntValueNode(TreeNode):
    pass

class FloatValueNode(TreeNode):
    pass

class CharValueNode(TreeNode):
    pass

class FunctionCallNode(TreeNode):
    pass

class ArgumentListNode(TreeNode):
    pass

class ComparatorNode(TreeNode):
    pass

class OperandNode(TreeNode):
    pass

class SumOperationNode(TreeNode):
    pass

class ProductOperationNode(TreeNode):
    pass

class OperationNode(TreeNode):
    pass

class IdentifierNode(TreeNode):
    pass

class TokenNode(TreeNode):
    def __init__(self, token):
        TreeNode.__init__(self)
        self.token = token

    def text(self):
        return str(self.token)
