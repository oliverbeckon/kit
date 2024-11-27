import lexer
import interpreter
import parser
# Create a lexer with the source code
source_code = """
x : "test"
for 5
say(x);
"""

# Step 1: Tokenize the source code
Mylexer = lexer.Lexer(source_code)
tokens = Mylexer.get_tokens()
print("Tokens:", tokens)

# Step 2: Parse the tokens into an AST
Myparser = parser.Parser(tokens)
ast = Myparser.parse()
for step in ast:
   print(type(step).__name__)

# Step 3: Interpret the AST
Myinterpreter = interpreter.Interpreter()
Myinterpreter.interpret(ast)
