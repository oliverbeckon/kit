#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "parser.c"

// The same AST and code generation setup from previous steps...

// Modify the generate_code function to output to a file
void generate_code(ASTNode *node, FILE *output_file) {
    if (node == NULL) return;

    switch (node->type) {
        case AST_NODE_NUMBER:
            fprintf(output_file, "PUSH %d\n", node->number_value);  // Push number onto stack
            break;

        case AST_NODE_IDENTIFIER:
            fprintf(output_file, "LOAD %s\n", node->identifier);  // Load variable
            break;

        case AST_NODE_BINARY_OP:
            generate_code(node->binary_op.left, output_file);
            generate_code(node->binary_op.right, output_file);
            switch (node->binary_op.op) {
                case BIN_OP_ADD:
                    fprintf(output_file, "ADD\n");
                    break;
                case BIN_OP_SUB:
                    fprintf(output_file, "SUB\n");
                    break;
                case BIN_OP_MUL:
                    fprintf(output_file, "MUL\n");
                    break;
                case BIN_OP_DIV:
                    fprintf(output_file, "DIV\n");
                    break;
                default:
                    fprintf(output_file, "UNKNOWN OPERATOR\n");
                    break;
            }
            break;

        case AST_NODE_ASSIGNMENT:
            generate_code(node->assignment.value, output_file);  // Generate code for the right-hand side expression
            fprintf(output_file, "STORE %s\n", node->assignment.identifier);  // Store result in variable
            break;

        case AST_NODE_RETURN:
            generate_code(node->assignment.value, output_file);  // Generate code for the return value
            fprintf(output_file, "RET\n");
            break;

        case AST_NODE_IF:
            generate_code(node->if_statement.condition, output_file);
            fprintf(output_file, "JUMP_IF_FALSE to ELSE\n");
            generate_code(node->if_statement.then_branch, output_file);
            if (node->if_statement.else_branch != NULL) {
                fprintf(output_file, "JUMP to END\n");
                fprintf(output_file, "ELSE:\n");
                generate_code(node->if_statement.else_branch, output_file);
            }
            fprintf(output_file, "END_IF:\n");
            break;

        default:
            fprintf(output_file, "UNKNOWN NODE TYPE\n");
            break;
    }
}
