import lexer
import interpreter
import parser
# Create a lexer with the source code
source_code = """

x = 234346456473453645674561933338


for i ++: 10 {
    say(x ** i)
}






"""

# Step 1: Tokenize the source code
Mylexer = lexer.Lexer(source_code)
tokens = Mylexer.get_tokens()
print(tokens)

# Step 2: Parse the tokens into an AST
Myparser = parser.Parser(tokens)
ast = Myparser.parse()

# Step 3: Interpret the AST
Myinterpreter = interpreter.Interpreter()
Myinterpreter.interpret(ast)
