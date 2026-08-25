#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_TOKEN_LEN 100
#define MAX_TOKENS 1000
#define MAX_SYMBOLS 100
#define MAX_CODE 1000

typedef enum {
    TOKEN_ID,        // 标识符
    TOKEN_NUM,       // 数字
    TOKEN_PLUS,      // +
    TOKEN_MINUS,     // -
    TOKEN_MULT,      // *
    TOKEN_DIV,       // /
    TOKEN_ASSIGN,    // =
    TOKEN_SEMICOLON, // ;
    TOKEN_LPAREN,    // (
    TOKEN_RPAREN,    // )
    TOKEN_EOF        // 文件结束
} TokenType;

// 词法单元结构
typedef struct {
    TokenType type;
    char lexeme[MAX_TOKEN_LEN];
} Token;

// 符号表项结构
typedef struct {
    char name[MAX_TOKEN_LEN];
    int is_temp;     // 是否为临时变量
    int temp_num;    // 临时变量编号
} Symbol;

// 三地址码结构
typedef struct {
    char op;         // 操作符
    char arg1[MAX_TOKEN_LEN];  // 操作数1
    char arg2[MAX_TOKEN_LEN];  // 操作数2
    char result[MAX_TOKEN_LEN]; // 结果
} ThreeAddressCode;

// 全局变量
char source_buffer[100000];  // 存储源文件内容
Token tokens[MAX_TOKENS];
int token_count = 0;
int current_token = 0;
Symbol symbol_table[MAX_SYMBOLS];
int symbol_count = 0;
ThreeAddressCode code[MAX_CODE];
int code_count = 0;
int temp_count = 0;

// 函数声明
void read_source_file(const char* filename);        // 读取源文件
void tokenize();                                    
void generate_code();                               // 中间代码生成
void print_code(const char* filename);              // 打印代码
char* get_new_temp();                               // 生成新的中间变量
int find_or_add_symbol(const char* name);           // 寻找或增加符号
void error(const char* msg);                        // 报错提示
void print_tokens();                                // 打印词法分析结果
// 递归下降解析器
char* expression();
char* term();
char* factor();


int main() {
    char input_file[MAX_TOKEN_LEN];
    char output_file[MAX_TOKEN_LEN];
    printf("please input the source file name: ");
    scanf("%s", input_file);
    printf("please input the target file name: ");
    scanf("%s", output_file);

    read_source_file(input_file);
    tokenize();
    print_tokens();  // 添加打印tokenize结果的调用
    generate_code();
    print_code(output_file);

    return 0;
}



// 修正后的 read_source_file 函数
void read_source_file(const char* filename) {
    char full_path[1000] = "./grammars/";
    strcat(full_path, filename);
    FILE* file = fopen(full_path, "r");
    if (!file) {
        error("cannot open source file");
    }
    size_t nread = fread(source_buffer, 1, sizeof(source_buffer) - 1, file);
    source_buffer[nread] = '\0';
    fclose(file);
}

// 修正后的 tokenize 函数
void tokenize() {
    token_count = 0;
    char* input = source_buffer;
    int pos = 0;

    while (input[pos] != '\0') {
        // 跳过空白字符
        while (isspace(input[pos])) pos++;
        if (input[pos] == '\0') break;

        // 识别标识符
        if (isalpha(input[pos])) {
            int start = pos;
            while (isalnum(input[pos])) pos++;
            strncpy(tokens[token_count].lexeme, &input[start], pos - start);
            tokens[token_count].lexeme[pos - start] = '\0';
            tokens[token_count].type = TOKEN_ID;
            token_count++;
        }
        // 识别数字
        else if (isdigit(input[pos])) {
            int start = pos;
            while (isdigit(input[pos])) pos++;
            strncpy(tokens[token_count].lexeme, &input[start], pos - start);
            tokens[token_count].lexeme[pos - start] = '\0';
            tokens[token_count].type = TOKEN_NUM;
            token_count++;
        }
        // 识别运算符
        else {
            switch (input[pos]) {
                case '+': tokens[token_count].type = TOKEN_PLUS; break;
                case '-': tokens[token_count].type = TOKEN_MINUS; break;
                case '*': tokens[token_count].type = TOKEN_MULT; break;
                case '/': tokens[token_count].type = TOKEN_DIV; break;
                case '=': tokens[token_count].type = TOKEN_ASSIGN; break;
                case ';': tokens[token_count].type = TOKEN_SEMICOLON; break;
                case '(': tokens[token_count].type = TOKEN_LPAREN; break;
                case ')': tokens[token_count].type = TOKEN_RPAREN; break;
                default: error("illegal character"); break;
            }
            tokens[token_count].lexeme[0] = input[pos];
            tokens[token_count].lexeme[1] = '\0';
            token_count++;
            pos++;
        }
    }

    // 添加 EOF token
    tokens[token_count].type = TOKEN_EOF;
    token_count++;
}


// 生成临时变量
char* get_new_temp() {
    char* temp = (char*)malloc(MAX_TOKEN_LEN);
    sprintf(temp, "t%d", ++temp_count);
    return temp;
}

// 表达式解析（加减）
char* expression() {
    char* op1 = term();
    while (tokens[current_token].type == TOKEN_PLUS 
            || tokens[current_token].type == TOKEN_MINUS) {
        char op = tokens[current_token].lexeme[0];
        current_token++;
        char* op2 = term();
        char* result = get_new_temp();
        // 生成三地址码
        strcpy(code[code_count].arg1, op1);
        strcpy(code[code_count].arg2, op2);
        strcpy(code[code_count].result, result);
        code[code_count].op = op;
        code_count++;
        op1 = result;
    }
    return op1;
}

// 项解析（乘除）
char* term() {
    char* op1 = factor();
    while (tokens[current_token].type == TOKEN_MULT 
            || tokens[current_token].type == TOKEN_DIV) {
        char op = tokens[current_token].lexeme[0];
        current_token++;
        char* op2 = factor();
        char* result = get_new_temp();
        strcpy(code[code_count].arg1, op1);
        strcpy(code[code_count].arg2, op2);
        strcpy(code[code_count].result, result);
        code[code_count].op = op;
        code_count++;
        op1 = result;
    }
    return op1;
}

// 因子解析（标识符/数字/括号）
char* factor() {
    char* result = NULL;
    if (tokens[current_token].type == TOKEN_ID || tokens[current_token].type == TOKEN_NUM) {
        result = strdup(tokens[current_token].lexeme);
        current_token++;
    } else if (tokens[current_token].type == TOKEN_LPAREN) {
        current_token++;
        result = expression();
        if (tokens[current_token].type != TOKEN_RPAREN) {
            error("lack of right parenthesis");
        }
        current_token++;
    } else {
        error("syntax error in factor");
    }
    return result;
}

// 中间代码生成
void generate_code() {
    current_token = 0;
    code_count = 0;
    while (tokens[current_token].type != TOKEN_EOF) {
        if (tokens[current_token].type == TOKEN_ID) {
            char target[MAX_TOKEN_LEN];
            strcpy(target, tokens[current_token].lexeme);
            current_token++;
            if (tokens[current_token].type == TOKEN_ASSIGN) {
                current_token++;
                char* expr_result = expression();
                // 生成赋值指令
                strcpy(code[code_count].arg1, expr_result);
                strcpy(code[code_count].result, target);
                code[code_count].op = '=';
                code_count++;
                // 跳过分号
                if (tokens[current_token].type == TOKEN_SEMICOLON) {
                    current_token++;
                }
            }
        } else {
            error("Grammar error");
        }
    }
}

void print_code(const char* filename) {
    char full_path[1000] = "./grammars/";
    strcat(full_path, filename);
    FILE* file = fopen(full_path, "w");
    if (!file) error("Cannot create the output file");
    printf("\nfinal geneal code: \n");
    for (int i = 0; i < code_count; i++) {
        if (code[i].op == '=') {
            fprintf(file, "%s = %s;\n", code[i].result, code[i].arg1);
            printf("%s = %s;\n", code[i].result, code[i].arg1);

        } else {
            fprintf(file, "%s = %s %c %s;\n", code[i].result, code[i].arg1, code[i].op, code[i].arg2);
            printf("%s = %s %c %s;\n", code[i].result, code[i].arg1, code[i].op, code[i].arg2);
        }
    }

    fclose(file);
}

// 打印词法分析结果
void print_tokens() {
    printf("\nToken Analysis Results:\n");
    printf("Type\t\tLexeme\n");
    printf("------------------------\n");
    
    for (int i = 0; i < token_count; i++) {
        printf("%-15s\t", 
            tokens[i].type == TOKEN_ID ? "IDENTIFIER" :
            tokens[i].type == TOKEN_NUM ? "NUMBER" :
            tokens[i].type == TOKEN_PLUS ? "PLUS" :
            tokens[i].type == TOKEN_MINUS ? "MINUS" :
            tokens[i].type == TOKEN_MULT ? "MULTIPLY" :
            tokens[i].type == TOKEN_DIV ? "DIVIDE" :
            tokens[i].type == TOKEN_ASSIGN ? "ASSIGN" :
            tokens[i].type == TOKEN_SEMICOLON ? "SEMICOLON" :
            tokens[i].type == TOKEN_EOF ? "EOF" : "UNKNOWN"
        );
        printf("%s\n", tokens[i].lexeme);
    }
    printf("------------------------\n");
    printf("Total tokens: %d\n", token_count);
}

// 错误处理
void error(const char* msg) {
    printf("error: %s\n", msg);
    exit(1);
} 