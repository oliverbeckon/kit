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
                #print(node.body[0].expression.right)
                self.variables[node.loopvar.identifier] = 0
                iterable = range(int(node.iterable.value))
                for node.loopvar.value in iterable:
                    self.variables[node.loopvar.identifier] += 1
                    self.interpret(node.body)
            elif isinstance(node, IfNode):

                if self.evaluate(node.expression) == True:
                    self.interpret(node.body)
                elif node.elseif != None:
                    self.interpret([node.elseif])
                elif node.els != None:
                    self.interpret(node.els)


    def evaluate(self, node):
        if isinstance(node, BooleanNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, BinOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if node.op in ["+", "-", "*", "/", "**", "%", "==", "!=", ">", "<", ">=", "<="]:
                #print(eval(f"{left} {node.op} {right}"))
                return eval(f"{left} {node.op} {right}")
            elif "//":
                return left**(1/right)
        elif isinstance(node, VariableNode):
            return self.variables[node.identifier]
        else:
            raise RuntimeError(f"Unknown node type: {node}")
