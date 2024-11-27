import re

TOKEN_TYPES = [
    ("NUMBER", r"\d+"),
    ("STRING", r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''),
    ("BOOLEAN", r"\b(True|False)\b"),

    ("PLUSEQUALTILL", r"\+\+:"),

    ("PLUSEQUAL", r"\+="),
    ("MINUSEQUAL", r"-="),
    ("TIMESEQUAL", r"\*="),
    ("DIVIDEEQUAL", r"/="),
    ("POWEREQUAL", r"\*\*="),
    ("SQAUREROOTEQUAL", r"//="),
    ("MODULASEQUAL", r"%="),

    ("ISEQUAL", r"=="),
    ("NOTEQUAL", r"!="),
    ("GREATER", r">"),
    ("LESS", r"<"),
    ("GREATEREQUAL", r">="),
    ("LESSEQUAL", r"<="),



    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("TIMES", r"\*"),
    ("DIVIDE", r"/"),
    ("POWER", r"\*\*"),
    ("SQUAREROOT", r"//"),
    ("MODULAS", r"%"),
    ("EQUALS", r"="),

    


    ("PRINT", r"say"),
    ("FOR", r"for"),
    ("BREAK", r";"),
    ("WHILE", r"while"),
    ("IF", r"\?"),
    ("ELSEIF", r"else\?"),
    ("ELSE", r"else"),
    ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z_0-9]*"),
    ("LEFTPAREN", r"\("),
    ("RIGHTPAREN", r"\)"),
    ("NEWLINE", r"\n"),
    ("SKIP", r"[ \t]+"),
    ("COMMENT", r"#.*"),
    ("MISMATCH", r".")
]

master_pattern = re.compile("|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in TOKEN_TYPES))


class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.tokenize()

    def tokenize(self):
        position = 0
        while position < len(self.source_code):
            match = None
            for token_type, regex in TOKEN_TYPES:
                regex_match = re.match(regex, self.source_code[position:])
                if regex_match:
                    match = regex_match.group(0)
                    if token_type == "SKIP" or token_type == "COMMENT" or token_type == "NEWLINE":
                        # Skip whitespace and comments (do not add them to tokens)
                        pass
                    else:
                        # Add all other tokens to the list
                        self.tokens.append((token_type, match))
                    position += len(match)
                    break
            if not match:
                raise SyntaxError(f"Unexpected character: {self.source_code[position]}")
            
    def get_tokens(self):
        return self.tokens  # Now this returns the list of tokens.
