from parser import AssignNode
from parser import PrintNode
from parser import NumberNode
from parser import BinOpNode
from parser import VariableNode

class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, ast):
        for node in ast:
            if isinstance(node, AssignNode):
                self.variables[node.identifier] = self.evaluate(node.value)
            elif isinstance(node, PrintNode):
                print(self.evaluate(node.expression))

    def evaluate(self, node):
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, BinOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if node.op == "+":
                return left + right
            elif node.op == "-":
                return left - right
            elif node.op == "*":
                return left * right
            elif node.op == "/":
                return left / right
            elif node.op == "//":
                return left**(1/right)
            elif node.op == "**":
                return left**right
            elif node.op == "%":
                return left % right
        elif isinstance(node, VariableNode):
            return self.variables[node.identifier]
        else:
            raise RuntimeError(f"Unknown node type: {node}")
