import lexer
import interpreter
import parser
# Create a lexer with the source code
source_code = """

func test() {
    say("i just called a function")
}

test()

"""

# Step 1: Tokenize the source code
Mylexer = lexer.Lexer(source_code)
tokens = Mylexer.get_tokens()
#print(tokens)

# Step 2: Parse the tokens into an AST
Myparser = parser.Parser(tokens)
ast = Myparser.parse()

# Step 3: Interpret the AST
Myinterpreter = interpreter.Interpreter()
Myinterpreter.interpret(ast)
