#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "ASTNodes.c"



// Parser structure
typedef struct Parser {
    const char *input;
    Token current_token;
} Parser;

// Function to initialize the parser
Parser *init_parser(const char *input) {
    Parser *parser = (Parser *)malloc(sizeof(Parser));
    parser->input = input;
    parser->current_token = get_next_token(&parser->input); // Get first token
    return parser;
}

// Function to advance the parser to the next token
void advance(Parser *parser) {
    parser->current_token = get_next_token(&parser->input);
}


// Function to parse a primary expression (identifier, number, etc.)
ASTNode *parse_primary(Parser *parser) {
    ASTNode *node = NULL;
    Token token = parser->current_token;
    
    // Check if it's a number
    if (token.type == TOKEN_NUMBER) {
        node = create_number_node(atoi(token.value));
        advance(parser);
    }
    // Check if it's an identifier (variable)
    else if (token.type == TOKEN_IDENTIFIER) {
        node = create_identifier_node(token.value);
        advance(parser);
    }
    return node;
}

// Function to parse binary operations
ASTNode *parse_binary_operation(Parser *parser, ASTNode *left) {
    Token token = parser->current_token;

    // Check for an operator (+, -, *, /)
    if (token.type == TOKEN_OPERATOR) {
        BinaryOperator op = BIN_OP_UNKNOWN;
        if (token.value[0] == '+') op = BIN_OP_ADD;
        else if (token.value[0] == '-') op = BIN_OP_SUB;
        else if (token.value[0] == '*') op = BIN_OP_MUL;
        else if (token.value[0] == '/') op = BIN_OP_DIV;

        advance(parser);
        
        // Parse the right-hand side of the operation
        ASTNode *right = parse_primary(parser);
        return create_binary_op_node(op, left, right);
    }
    
    return left;
}

// Function to parse an expression (handles binary operations)
ASTNode *parse_expression(Parser *parser) {
    ASTNode *left = parse_primary(parser);
    return parse_binary_operation(parser, left);
}

// Function to parse a statement
ASTNode *parse_statement(Parser *parser) {
    ASTNode *node = NULL;
    Token token = parser->current_token;
    
    if (token.type == TOKEN_KEYWORD && strcmp(token.value, "return") == 0) {
        advance(parser); // Skip 'return'
        node = create_return_node(parse_expression(parser));
    }
    return node;
}

int main() {
    const char *input = "return x + 3;";
    
    // Initialize lexer and parser

    Parser *parser = init_parser(input);
    
    // Parse a statement (for now, we just handle simple "return" statements)
    ASTNode *ast = parse_statement(parser);

    // Output the AST node type (just for testing)
    if (ast) {
        printf("parsed node");
    }
    
    return 0;
}
