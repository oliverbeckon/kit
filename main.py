import kitLexer
import kitInterpreter
import kitParser
# Create a lexer with the source code
source_code = """

func test(value, value2, value3) {
    say(value)
    say(value2)
    say(value3)
}

test('test', 10, 10 + 3)
   

func test2(value) {

    say(value)
}

test2(100000)
"""

# Step 1: Tokenize the source code
Mylexer = kitLexer.Lexer(source_code)
tokens = Mylexer.get_tokens()
print(tokens)

# Step 2: Parse the tokens into an AST
Myparser = kitParser.Parser(tokens)
ast = Myparser.parse()

# Step 3: Interpret the AST
Myinterpreter = kitInterpreter.Interpreter()
Myinterpreter.interpret(ast)
