#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "lexer.c"

#define MAX_TOKEN_LENGTH 100

// AST Node types
typedef enum {
    AST_NODE_UNKNOWN,
    AST_NODE_NUMBER,
    AST_NODE_IDENTIFIER,
    AST_NODE_BINARY_OP,
    AST_NODE_ASSIGNMENT,
    AST_NODE_RETURN,
    AST_NODE_IF
} ASTNodeType;

// Binary operators (for AST)
typedef enum {
    BIN_OP_ADD, BIN_OP_SUB, BIN_OP_MUL, BIN_OP_DIV, BIN_OP_UNKNOWN
} BinaryOperator;

// AST Node structure
typedef struct ASTNode {
    ASTNodeType type;
    union {
        int number_value;             // For number nodes
        char identifier[MAX_TOKEN_LENGTH];  // For identifier nodes (e.g., variables)
        struct {
            BinaryOperator op;         // The operator in a binary operation
            struct ASTNode *left;      // Left operand
            struct ASTNode *right;     // Right operand
        } binary_op;
        struct {
            char identifier[MAX_TOKEN_LENGTH]; // Variable being assigned
            struct ASTNode *value;     // Expression or value assigned to variable
        } assignment;
        struct {
            struct ASTNode *condition; // Expression for the condition
            struct ASTNode *then_branch; // Branch for "true" condition
            struct ASTNode *else_branch; // Branch for "false" condition (optional)
        } if_statement;
    };
} ASTNode;

// Function to create a new AST Node for a number
ASTNode *create_number_node(int value) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->type = AST_NODE_NUMBER;
    node->number_value = value;
    return node;
}

// Function to create a new AST Node for an identifier (variable)
ASTNode *create_identifier_node(const char *id) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->type = AST_NODE_IDENTIFIER;
    strcpy(node->identifier, id);
    return node;
}

// Function to create a new AST Node for a binary operation
ASTNode *create_binary_op_node(BinaryOperator op, ASTNode *left, ASTNode *right) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->type = AST_NODE_BINARY_OP;
    node->binary_op.op = op;
    node->binary_op.left = left;
    node->binary_op.right = right;
    return node;
}

// Function to create a new AST Node for assignment
ASTNode *create_assignment_node(const char *identifier, ASTNode *value) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->type = AST_NODE_ASSIGNMENT;
    strcpy(node->assignment.identifier, identifier);
    node->assignment.value = value;
    return node;
}

// Function to create a new AST Node for return statement
ASTNode *create_return_node(ASTNode *value) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->type = AST_NODE_RETURN;
    node->assignment.value = value; // "value" here is the return expression
    return node;
}

// Function to create a new AST Node for if statement
ASTNode *create_if_node(ASTNode *condition, ASTNode *then_branch, ASTNode *else_branch) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->type = AST_NODE_IF;
    node->if_statement.condition = condition;
    node->if_statement.then_branch = then_branch;
    node->if_statement.else_branch = else_branch;
    return node;
}
