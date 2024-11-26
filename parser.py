class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = int(value)

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class AssignNode(ASTNode):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

class PrintNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def eat(self, token_type):
        if self.current_token() and self.current_token()[0] == token_type:
            self.pos += 1
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token()}")
    
    def parse(self):
        nodes = []
        while self.pos < len(self.tokens):
            if self.current_token()[0] == "IDENTIFIER":
                nodes.append(self.parse_assign())
            elif self.current_token()[0] == "PRINT":
                nodes.append(self.parse_print())
            else:
                raise SyntaxError(f"Unexpected token: {self.current_token()}")
        return nodes
    
    def parse_assign(self):
        identifier = self.current_token()[1]
        self.eat("IDENTIFIER")
        self.eat("EQUALS")
        value = self.parse_expression()
        return AssignNode(identifier, value)
    
    def parse_print(self):
        self.eat("PRINT")
        self.eat("LEFTPAREN")
        expression = self.parse_expression()
        self.eat("RIGHTPAREN")
        return PrintNode(expression)
    
    def parse_expression(self):
        node = self.parse_term()
        while self.current_token() and self.current_token()[0] in ("PLUS", "MINUS", "MODULAS"):
            op = self.current_token()[1]
            self.eat(op)
            right = self.parse_term()
            node = BinOpNode(node, op, right)
        return node
    
    def parse_term(self):
        node = self.parse_factor()
        while self.current_token() and self.current_token()[0] in ("TIMES", "DIVIDE", "POWER", "SQUAREROOT"):
            op = self.current_token()[1]
            self.eat(op)
            right = self.parse_factor()
            node = BinOpNode(node, op, right)
        return node
    
    def parse_factor(self):
        if self.current_token()[0] == "NUMBER":
            value = self.current_token()[1]
            self.eat("NUMBER")
            return NumberNode(value)
        elif self.current_token()[0] == "IDENTIFIER":
            value = self.current_token()[1]
            self.eat("IDENTIFIER")
            return NumberNode(value)  # Treat as a variable reference for now
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token()}")
