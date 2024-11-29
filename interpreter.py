from parser import *




class Enviroment:
    def __init__(self, parent=None) -> None:
        self.scopeVariables = {}
        self.parent = parent
    
    def set(self, name, value):
        self.scopeVariables[name] = value
    
    def get(self, name):
        if name in self.scopeVariables:
            return self.scopeVariables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Undefined variable: {name}")
        
    def add(self, name, value):
        self.scopeVariables[name] = self.get(name) + value





class Interpreter:

    def __init__(self):
        self.env = Enviroment()

    def interpret(self, ast, env = None):
        if env == None:
            env = self.env

        for node in ast:
            if isinstance(node, AssignNode):
                env.set(node.identifier, self.evaluate(node.value))


            elif isinstance(node, PrintNode):
                print(self.evaluate(node.expression))


            elif isinstance(node, ForNode):

                env.set(node.loopvar.identifier, 0)
                iterable = range(int(node.iterable.value))
                for i in iterable:
                    env.add(node.loopvar.identifier, 1)
                    self.interpret(node.body)


            elif isinstance(node, IfNode):
                if self.evaluate(node.expression) == True:
                    self.interpret(node.body)
                elif node.elseif != None:
                    self.interpret([node.elseif])
                elif node.els != None:
                    self.interpret(node.els)


            elif isinstance(node, WhileNode):
                while self.evaluate(node.expression) == True:
                    self.interpret(node.body)


            elif isinstance(node, FunctionNode):
                env.set(self.evaluate(node.identifier), node)


            elif isinstance(node, FunctionCallNode):
                funcDecl = env.get(node.identifier)

                localEnv = Enviroment(parent=env)
                args = []
                for arg in funcDecl.args:
                    args.append(self.evaluate(arg))
                
                #if funcDecl.args != None:
                   # for param, arg in zip(args, node.args):
                    #    value = self.evaluate(arg)
                    #    localEnv.set(param, value)

                self.interpret(funcDecl.body, localEnv)

            elif isinstance(node, ReturnNode):
                return self.evaluate(node.expression)
                




    def evaluate(self, node, env = None):
        if env == None:
            env = self.env
        if node == None:
            return None

        if isinstance(node, BooleanNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, BinOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if node.op in ["+", "-", "*", "/", "**", "%", "==", "!=", ">", "<", ">=", "<=", "and", "or"]:
                return eval(f"{left} {node.op} {right}")
            elif "//":
                return left**(1/right)
        elif isinstance(node, VariableNode):
            return env.get(node.identifier)
        else:
            raise RuntimeError(f"Unknown node type: {node}")
