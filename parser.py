class ASTNode:
    pass


class ForNode(ASTNode):
    def __init__(self, loopvar, iterable, body):
        self.loopvar = loopvar
        self.iterable = iterable
        self.body = body

class IfNode(ASTNode):
    def __init__(self, expression, body, elseif, els):
        self.expression = expression
        self.body = body
        self.elseif = elseif
        self.els = els

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
    def __init__(self, identifier, value, glob= False):
        self.identifier = identifier
        self.value = value
        self.glob = glob

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


    def create_default(self, variable, cls):
        match cls:
            case "BOOLEAN":
                return BooleanNode(variable)
            case "STRING":
                return StringNode(variable)
            case "NUMBER":
                return NumberNode(variable)
            case "IDENTIFIER":
                return VariableNode(variable)
            

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
            match self.current_token[0]:
                case "PRINT":
                    statements.append(self.parse_print())
                case "IDENTIFIER":
                    statements.append(self.parse_assignment())
                case "FOR":
                    statements.append(self.parse_loop())
                case "IF":
                    statements.append(self.parse_if())
                case "WHILE":
                    statements.append(self.parse_while())
                case _:
                    self.advance()  # Skip any unexpected tokens
        return statements

    def parse_block(self):
        self.advance()
        statements = []
        while self.current_token[0] != "ENDBLOCK":
            match self.current_token[0]:
                case "PRINT":
                    statements.append(self.parse_print())
                case "IDENTIFIER":
                    statements.append(self.parse_assignment())
                case "FOR":
                    statements.append(self.parse_loop())
                case "IF":
                    statements.append(self.parse_if())
                case _:
                    self.advance()  # Skip any unexpected 
        self.advance()
        return statements


    def parse_while(self):
        self.advance()
        condition = self.parse_condition()
        body = self.parse_block()
        return WhileNode(condition, body)



    def parse_if(self):
        elseif = None
        els = None
        self.advance()
        condition = self.parse_condition()
        body = self.parse_block()
        if self.current_token != None:
            if self.current_token[0] == "ELSE": 
                self.advance()
                if self.current_token[0] == "IF":
                    elseif = self.parse_if()
                elif self.current_token[0] == "STARTBLOCK":
                    els = self.parse_block()
        return IfNode(condition, body, elseif, els)
        


    def parse_loop(self):
        var = None
        self.advance()
        iterable = self.create_default(self.current_token[1], self.current_token[0])
        self.advance()
        if self.current_token[0] == "PLUSEQUALTILL":
            var = iterable
            self.advance()
            iterable = self.parse_expression()
        body = self.parse_block()

        return ForNode(var, iterable, body)



    def parse_assignment(self):
        name = self.current_token[1]
        self.advance()
        self.advance()
        value = self.parse_expression()
        return AssignNode(name, value)


    def parse_print(self):
        """Parse Print"""
        self.advance()
        if self.current_token[0] != "LEFTPAREN":
             raise SyntaxError("Expected '(' after say")
        self.advance()
        expr = self.parse_parentheses()
        return PrintNode(expr)
    

    def parse_parentheses(self):
        left = None
        while self.current_token[0] != "RIGHTPAREN":
            if self.current_token[0] in ["STRING", "IDENTIFIER", "BOOLEAN"]:
                if left == None:
                    left = self.create_default(self.current_token[1], self.current_token[0])
                    self.advance()
                else:
                    raise SystemError(f"Unexpected token in parentheses: {self.current_token[0]}")
            elif self.current_token[0] in ["DIVIDE", "TIMES", "POWER", "SQUAREROOT", "MODULAS"]:
                op = self.current_token[1]
                self.advance()
                right = self.parse_expression()
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
        elif self.current_token[0] in ["IDENTIFIER", "NUMBER", "BOOLEAN", "STRING"]:
            left = self.create_default(self.current_token[1], self.current_token[0])
            self.advance()
        elif self.current_token[0] == "ENDBLOCK":
            self.advance()
            return left
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token[0]}")
        

        if self.current_token[0] in ["PLUS", "MINUS", "DIVIDE", "TIMES", "POWER", "SQUAREROOT", "MODULAS"]:
            op = self.current_token[1]
            self.advance()
            right = self.parse_expression()
            left = BinOpNode(left, op, right)
           
        return left
    
    
    def parse_condition(self) -> BinOpNode | None:
        left = self.parse_expression()
        if self.current_token[0] in ["ISEQUAL", "NOTEQUAL", "GREATER", "LESS", "GREATEREQUAL", "LESSEQUAL"]:
            op = self.current_token[1]
            self.advance()
            right = self.parse_expression()
            left = BinOpNode(left, op, right)

        if self.current_token[0] in ["OR", "AND"]:
            op = self.current_token[1]
            self.advance()
            right = self.parse_condition()
            left = BinOpNode(left, op, right)

        return left

    
   
  
  


     