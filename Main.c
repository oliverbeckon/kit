#include "codeGen.c"


int main() {
    const char *input = "return 6 + 3;";
    
    // Initialize lexer and parser

    Parser *parser = init_parser(input);
    
    // Parse a statement (for now, we just handle simple "return" statements)
    ASTNode *ast = parse_statement(parser);

    // Write assembly output to a file
    FILE *output_file = fopen("program.s", "w");
    if (output_file == NULL) {
        fprintf(stderr, "Error opening file for writing.\n");
        return 1;
    }

    generate_code(ast, output_file);
    
    fclose(output_file);

    // gcc -c program.s -o program.o

    return 0;
}
