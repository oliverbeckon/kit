from parser import *

class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, ast):
        for node in ast:
            if isinstance(node, AssignNode):
                self.variables[node.identifier] = self.evaluate(node.value)
            elif isinstance(node, PrintNode):
                print(self.evaluate(node.expression))
            elif isinstance(node, ForNode):
                iterable = range(int(node.iterable.value))
                for x in iterable:
                    self.interpret(node.body)
            elif isinstance(node, IfNode):
                if self.evaluate(node.expression) == True:
                    self.interpret(node.body)


    def evaluate(self, node):
        if isinstance(node, BooleanNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value[1:-1]
        elif isinstance(node, NumberNode):
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
            
        elif isinstance(node, BoolOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if node.op == "::":
                return left == right
            elif node.op == "!=":
                return left != right
            elif node.op == ">":
                return left > right
            elif node.op == "<":
                return left < right
            elif node.op == ">:":
                return left >= right
            elif node.op == "<:":
                return left <= right

        elif isinstance(node, StrOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if node.op == "+":
                return left + str(right)
            if node.op == "*":
                if isinstance(right, NumberNode) or isinstance(right, VariableNode):
                    newleft = left
                    for i in range(right):
                        newleft += left
                    return newleft
                else:
                    raise RuntimeError(f"String {left} cannot be mutiplied by {right}. Strings can only be mutiplied by ints")
        elif isinstance(node, VariableNode):
            return self.variables[node.identifier]
        else:
            raise RuntimeError(f"Unknown node type: {node}")
