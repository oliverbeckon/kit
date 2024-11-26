import re

TOKEN_TYPES = [
    ("NUMBER", r"\d+"),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("TIMES", r"\*"),
    ("DIVIDE", r"/"),
    ("POWER", r"\**"),
    ("SQUAREROOT", r"//"),
    ("MODULAS", r"%"),
    ("EQUALS", r":"),
    ("PRINT", r"say"),
    ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z_0-9]*"),
    ("LEFTPAREN", r"\("),
    ("RIGHTPAREN", r"\)"),
    ("NEWLINE", r"\n"),
    ("SKIP", r"[ \t]+"),
    ("COMMENT", r"#.*"),
    ("MISMATCH", r".")
]

master_pattern = re.compile("|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in TOKEN_TYPES))


def lex(code):
    pos = 0
    tokens = []
    
    while pos < len(code):
        match = master_pattern.match(code, pos)
        if match:
            type_ = match.lastgroup
            value = match.group(type_)
            if type_ == "SKIP" or type_ == "COMMENT":
                pass  # Ignore spaces and comments
            elif type_ != "MISMATCH":
                tokens.append((type_, value))
            pos = match.end()
        else:
            raise SyntaxError(f"Unexpected character at position {pos}")
    
    return tokens
