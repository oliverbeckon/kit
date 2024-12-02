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




class FunctionNode(ASTNode):
    def __init__(self, identifier, body, args = None) -> None:
        self.identifier = identifier
        self.args = args
        self.body = body

class FunctionCallNode(ASTNode):
    def __init__(self, identifier, args = None) -> None:
        self.identifier = identifier
        self.args = args

class ReturnNode(ASTNode):
    def __init__(self, value) -> None:
        self.value = value





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
                case "FUNCTION":
                    statements.append(self.parse_func())
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
                case "RETURN":
                    self.advance()
                    statements.append(self.parse_expression())
                case _:
                    self.advance()  # Skip any unexpected 
        self.advance()
        return statements


    def parse_func(self):
        self.advance()
        identifier = self.parse_String() # Get Name of func
        self.advance()
        self.advance()
        args = self.parse_args()
        self.advance()
        body = self.parse_block()
        return FunctionNode(identifier, body, args)



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
        if self.current_token[0] == "PLUSPLUSTILL":
            var = iterable
            self.advance()
            iterable = self.parse_expression()
        body = self.parse_block()

        return ForNode(var, iterable, body)



    def parse_assignment(self):
        identifier = self.current_token[1]
        self.advance()
        if self.current_token[0] == "LEFTPAREN":
            return self.parse_functionCall(identifier)
        
        elif self.current_token[0] in ["PLUS", "MINUS", "TIMES"]:
            value = self.parse_expression(VariableNode(identifier))

        else:
            self.advance()
            value = self.parse_expression()

        return AssignNode(identifier, value)


    def parse_print(self):
        """Parse Print"""
        self.advance()
        if self.current_token[0] != "LEFTPAREN":
             raise SyntaxError("Expected '(' after say")
        self.advance()
        expr = self.parse_expression()
        self.advance()
        return PrintNode(expr)
    
    
    def parse_expression(self, left = None) -> BinOpNode | VariableNode | NumberNode | StringNode | BooleanNode | None:
        if self.current_token[0] == "LEFTPAREN":
            self.advance()
            left = self.parse_expression()
        elif self.current_token[0] == "RIGHTPAREN":
            return left
        elif self.current_token[0] in ["IDENTIFIER", "NUMBER", "BOOLEAN", "STRING"]:
            left = self.create_default(self.current_token[1], self.current_token[0])
            self.advance()
        elif self.current_token[0] == "ENDBLOCK":
            self.advance()
            return 
        elif self.current_token[0] in ["PLUS", "MINUS", "DIVIDE", "TIMES", "POWER", "SQUAREROOT", "MODULAS"]:
            op = self.current_token[1]
            self.advance()
            if self.current_token[0] == "EQUALS":
                self.advance()
                right = self.parse_expression()
                left = BinOpNode(left, op, right)
                return left
            else:
                raise SyntaxError(f"Unexpected token: {self.current_token[0]}")
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token[0]}")
        
        if self.current_token[0] == "EQUALS":
            self.advance()
            value = self.parse_expression()
            return AssignNode(left, value)



        if self.current_token[0] in ["PLUS", "MINUS", "DIVIDE", "TIMES", "POWER", "SQUAREROOT", "MODULAS"]:
            op = self.current_token[1]
            self.advance()
            if self.current_token[0] == "EQUALS":
                self.advance()
                right = self.parse_expression()
                newleft = BinOpNode(left, op, right)
                left =  AssignNode(left, newleft)
            else:
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

    
    def parse_String(self):
        return self.create_default(self.current_token[1], "STRING")


    def parse_args(self):
        args = []
        while self.current_token and self.current_token[0] != "RIGHTPAREN":
            if self.current_token[0] != "COMMA":
                args.append(self.parse_String())
            self.advance()
        return args


    def parse_functionCall(self, identifier):
        self.advance()
        args = []
        while self.current_token and self.current_token[0] != "RIGHTPAREN":
            if self.current_token[0] != "COMMA":
                args.append(self.parse_expression())
            else :
                self.advance()

        return FunctionCallNode(identifier, args)
     

        

  
  


     