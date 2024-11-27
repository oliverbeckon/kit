class ASTNode:
    pass


class ForNode(ASTNode):
    def __init__(self, loopvar, iterable, body):
        self.loopvar = loopvar
        self.iterable = iterable
        self.body = body

class IfNode(ASTNode):
    def __init__(self, expression, body):
        self.expression = expression
        self.body = body

class WhileNode(ASTNode):
    def __init__(self, expression, body):
        self.expression = expression
        self.body = body


class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = int(value)

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = str(value)

class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = bool(value)
        


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
        
class StrOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class BoolOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


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
            elif self.current_token[0] == "IF":
                statements.append(self.parse_if())
            else:
                self.advance()  # Skip any unexpected tokens
        return statements

    def parse_tillBreak(self):
        statements = []
        while self.current_token[0] != "BREAK":
            if self.current_token[0] == "PRINT":
                self.advance()
                statements.append(self.parse_print())
            elif self.current_token[0] == "IDENTIFIER":
                statements.append(self.parse_assignment())
            elif self.current_token[0] == "FOR":
                statements.append(self.parse_loop())
            elif self.current_token[0] == "IF":
                statements.append(self.parse_if())
            else:
                self.advance()  # Skip any unexpected tokens
        return statements



    def parse_if(self):
        self.advance()
        expression = self.parse_expression()

        body = self.parse_tillBreak()
        return IfNode(expression, body)
        


    def parse_loop(self):
        self.advance()
        if self.current_token[0] == "IDENTIFIER":
            iterable = VariableNode(self.current_token[1])
        elif self.current_token[0] == "NUMBER":
            iterable = NumberNode(self.current_token[1])
        
        body = self.parse_tillBreak()
        
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
        return PrintNode(expr)
    
    def parse_parentheses(self):
        left = None
        while self.current_token[0] != "RIGHTPAREN":
            if self.current_token[0] == "STRING":
                if left == None:
                    left = StringNode(self.current_token[1])
                    self.advance()
                else:
                    raise SystemError(f"Unexpected token in parentheses: {self.current_token[0]}")
            elif self.current_token[0] == "IDENTIFIER":
                if left == None:
                    left = VariableNode(self.current_token[1])
                    self.advance()
                else:
                    raise SyntaxError(f"Unexpected token in parentheses: {self.current_token[0]}")
            elif self.current_token[0] == "BOOLEAN":
                if left == None:
                    left = BooleanNode(self.current_token[1])
                    self.advance()
                else:
                    raise SyntaxError(f"Unexpected token in parentheses: {self.current_token[0]}")
            elif self.current_token[0] in ["DIVIDE", "TIMES", "POWER", "SQUAREROOT"]:
                op = self.current_token[1]
                self.advance()
                right = self.parse_expression()
                self.advance()
                left = BinOpNode(left, op, right)
            elif self.current_token[0] in ["PLUS", "MINUS"]:
                op = self.current_token[1]
                self.advance()
                right = self.parse_expression()
                left = BinOpNode(left, op, right)


        return left
    
    def parse_expression(self) -> BinOpNode | VariableNode | NumberNode | StringNode | BooleanNode | None:
        left = None
        if self.current_token[0] == "LEFTPAREN":
            left = self.parse_parentheses()
            self.advance()
        elif self.current_token[0] == "IDENTIFIER":
            left = VariableNode(self.current_token[1])
            self.advance()
        elif self.current_token[0] == "NUMBER":
            left = NumberNode(self.current_token[1])
            self.advance()
        elif self.current_token[0] == "STRING":
            left = StringNode(self.current_token[1])
            self.advance()
        elif self.current_token[0] == "BOOLEAN":
            left = BooleanNode(self.current_token[1])
            self.advance()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token[0]}")
        

        if isinstance(left, StringNode) and self.current_token[0] in ["PLUS", "TIMES"]:
            op = self.current_token[1]
            self.advance()
            right = self.parse_expression()
            left = StrOpNode(left, op, right)
        elif self.current_token[0] in ["PLUS", "MINUS", "DIVIDE", "TIMES", "POWER", "SQUAREROOT"]:
            op = self.current_token[1]
            self.advance()
            right = self.parse_expression()
            left = BinOpNode(left, op, right)
        elif self.current_token[0] in ["ISEQUAL", "NOTEQUAL", "GREATER", "LESS", "GREATEREQUAL", "LESSEQUAL"]:
            op = self.current_token[1]
            self.advance()
            right = self.parse_expression()
            left = BoolOpNode(left, op, right)
        
        return left
    
    def parse_factor(self) -> VariableNode | NumberNode:
        if self.current_token[0] == "IDENTIFIER":
            return VariableNode(self.current_token[1])
        elif self.current_token[0] == "NUMBER":
            return NumberNode(self.current_token[1])
  
  


     