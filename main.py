import lexer
import interpreter
import parser
# Create a lexer with the source code
source_code = """
? True {
    say('test')
}
for i ++: 100 {
    z = i % 5 + i % 3
    ? z == 0 {
        say("FizzBuzz")
    } else? i % 5 == 0 {
        say("Buzz")
    } else? i % 3 == 0 {
        say("Fizz")
    } else {
        say(i) 
    }
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
