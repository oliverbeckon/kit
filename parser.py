class ASTNode:
    pass


class ForNode(ASTNode):
    def __init__(self, loopvar, iterable, body):
        self.loopvar = loopvar
        self.iterable = iterable
        self.body = body


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

class VariableNode(ASTNode):
    def __init__(self, identifier):
        self.identifier = identifier
        





class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = -1
        self.advance()

    def advance(self):
        """Move to the next token."""
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def parse(self):
        """Start parsing an expression."""
        return self.parse_program()

    def parse_program(self):
        """Parse the program, which can be a print or an assignment."""
        statements = []
        while self.current_token:
            if self.current_token[0] == "PRINT":
                self.advance()
                statements.append(self.parse_print())
            elif self.current_token[0] == "IDENTIFIER":
                statements.append(self.parse_assignment())
            elif self.current_token[0] == "FOR":
                statements.append(self.parse_loop())
            else:
                self.advance()  # Skip any unexpected tokens
        return statements


    def parse_loop(self):
        self.advance()
        if self.current_token[0] == "IDENTIFIER":
            iterable = VariableNode(self.current_token[1])
        elif self.current_token[0] == "NUMBER":
            iterable = NumberNode(self.current_token[1])
        
        body = []
        while self.current_token[0] != "FOREND":
            if self.current_token[0] == "PRINT":
                self.advance()
                body.append(self.parse_print())
            elif self.current_token[0] == "IDENTIFIER":
                body.append(self.parse_assignment())
            elif self.current_token[0] == "FOR":
                body.append(self.parse_loop())
            else:
                self.advance()  # Skip any unexpected tokens
        
        return ForNode(None, iterable, body)



    def parse_assignment(self):
        name = self.current_token[1]
        self.advance()
        self.advance()
        value = self.parse_expression()
        return AssignNode(name, value)

    def parse_print(self):
        """Parse Print"""
        if self.current_token[0] != "LEFTPAREN":
             raise SyntaxError("Expected '(' after say")
        self.advance()
        expr = self.parse_parentheses()
        print(f"Expr: {expr}")
        return PrintNode(expr)
    
    def parse_parentheses(self):
        left = None
        while self.current_token[0] != "RIGHTPAREN":
            if self.current_token[0] == "IDENTIFIER":
                if left == None:
                    left = VariableNode(self.current_token[1])
                    self.advance()
                else:
                    print(left)
                    raise SyntaxError(f"Unexpected token in parentheses: {self.current_token[0]}")
            elif self.current_token[0] in ["DIVIDE", "TIMES", "POWER", "SQUAREROOT"]:
                op = self.current_token[1]
                self.advance()
                right = self.parse_factor()
                self.advance()
                left = BinOpNode(left, op, right)
            elif self.current_token[0] in ["PLUS", "MINUS"]:
                op = self.current_token[1]
                self.advance()
                right = self.parse_expression()
                left = BinOpNode(left, op, right)

        print(f"parentheses expr: {left}")
        return left
    
    def parse_expression(self) -> BinOpNode | VariableNode | NumberNode | None:
        left = None
        if self.current_token[0] == "IDENTIFIER":
            left = VariableNode(self.current_token[1])
            self.advance()
        elif self.current_token[0] == "NUMBER":
            left = NumberNode(self.current_token[1])
            self.advance()
        else:
            raise SyntaxError(f"Unexpected token in say function: {self.current_token[0]}")
        
        if self.current_token[0] in ["PLUS", "MINUS", "DIVIDE", "TIMES", "POWER", "SQUAREROOT"]:
            op = self.current_token[1]
            self.advance()
            right = self.parse_expression()
            left = BinOpNode(left, op, right)

        
        return left
    
    def parse_factor(self) -> VariableNode | NumberNode:
        if self.current_token[0] == "IDENTIFIER":
            return VariableNode(self.current_token[1])
        elif self.current_token[0] == "NUMBER":
            return NumberNode(self.current_token[1])
  
  


     