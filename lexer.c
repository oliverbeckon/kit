#include <stdio.h>
#include <ctype.h>
#include <string.h>

#define MAX_TOKEN_LENGTH 100

// Token types
typedef enum {
    TOKEN_UNKNOWN, TOKEN_KEYWORD, TOKEN_IDENTIFIER, TOKEN_NUMBER, TOKEN_OPERATOR, TOKEN_SEPARATOR, TOKEN_END
} TokenType;

// Token structure
typedef struct {
    TokenType type;
    char value[MAX_TOKEN_LENGTH];
} Token;

// Keywords list
const char *keywords[] = { "if", "else", "while", "return", NULL };

// Function to check if a string is a keyword
int is_keyword(const char *str) {
    for (int i = 0; keywords[i] != NULL; i++) {
        if (strcmp(str, keywords[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

// Function to classify a character
int is_operator(char c) {
    return c == '+' || c == '-' || c == '*' || c == '/';
}

int is_separator(char c) {
    return c == '(' || c == ')' || c == '{' || c == '}' || c == ';';
}

// Lexer function to extract the next token
Token get_next_token(const char **input) {
    Token token;
    token.type = TOKEN_UNKNOWN;
    token.value[0] = '\0';

    // Skip whitespace
    while (isspace(**input)) {
        (*input)++;
    }

    if (**input == '\0') {
        token.type = TOKEN_END;
        return token;
    }

    // Identifiers or keywords
    if (isalpha(**input)) {
        int i = 0;
        while (isalnum(**input) || **input == '_') {
            token.value[i++] = **input;
            (*input)++;
        }
        token.value[i] = '\0';
        if (is_keyword(token.value)) {
            token.type = TOKEN_KEYWORD;
        } else {
            token.type = TOKEN_IDENTIFIER;
        }
        return token;
    }

    // Numbers
    if (isdigit(**input)) {
        int i = 0;
        while (isdigit(**input)) {
            token.value[i++] = **input;
            (*input)++;
        }
        token.value[i] = '\0';
        token.type = TOKEN_NUMBER;
        return token;
    }

    // Operators
    if (is_operator(**input)) {
        token.value[0] = **input;
        token.value[1] = '\0';
        token.type = TOKEN_OPERATOR;
        (*input)++;
        return token;
    }

    // Separators
    if (is_separator(**input)) {
        token.value[0] = **input;
        token.value[1] = '\0';
        token.type = TOKEN_SEPARATOR;
        (*input)++;
        return token;
    }

    // Default case for unknown characters
    token.value[0] = **input;
    token.value[1] = '\0';
    token.type = TOKEN_UNKNOWN;
    (*input)++;
    return token;
}

// Main lexer loop
void lex(const char *input) {
    Token token;
    while (1) {
        token = get_next_token(&input);
        if (token.type == TOKEN_END) {
            break;
        }

        // Output token information
        switch (token.type) {
            case TOKEN_KEYWORD:
                printf("KEYWORD: %s\n", token.value);
                break;
            case TOKEN_IDENTIFIER:
                printf("IDENTIFIER: %s\n", token.value);
                break;
            case TOKEN_NUMBER:
                printf("NUMBER: %s\n", token.value);
                break;
            case TOKEN_OPERATOR:
                printf("OPERATOR: %s\n", token.value);
                break;
            case TOKEN_SEPARATOR:
                printf("SEPARATOR: %s\n", token.value);
                break;
            default:
                printf("UNKNOWN: %s\n", token.value);
                break;
        }
    }
}

int main() {
    const char *input = "if (x + 3) return y;";
    lex(input);
    return 0;
}
