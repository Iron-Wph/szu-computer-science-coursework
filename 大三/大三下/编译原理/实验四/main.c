#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <locale.h>
#define MAX_PROD_LEN 100
#define MAX_SYMBOLS 100
#define MAX_STATES 100
#define MAX_ITEMS 100
// 产生式结构
typedef struct {
    char left[MAX_PROD_LEN];    // 左部
    char right[MAX_PROD_LEN];   // 右部
    int dot_pos;                // 点的位置
} Production;

// LR(0)项目结构
typedef struct {
    Production prod;
    bool is_reduce;             // 是否为归约项目
} LR0Item;

// 项目集结构
typedef struct {
    LR0Item items[MAX_ITEMS];
    int item_count;
} ItemSet;

// DFA状态结构
typedef struct {
    ItemSet item_set;
    int state_id;
    int transitions[MAX_SYMBOLS];  // 转移表
} DFAState;

// 分析表项结构
typedef struct {
    char action;                // 's'表示移进，'r'表示归约，'a'表示接受
    int value;                  // 状态号或产生式编号
} TableEntry;

// 全局变量
Production grammar[MAX_PROD_LEN];
int prod_count = 0;
DFAState dfa_states[MAX_STATES];
int state_count = 0;
TableEntry action_table[MAX_STATES][MAX_SYMBOLS];
TableEntry goto_table[MAX_STATES][MAX_SYMBOLS];

// 函数声明
void read_grammar();                        // 读取文法
void extend_grammar();                      // 扩展文法
ItemSet closure(ItemSet set);               // 计算闭包
void construct_dfa();                       // 构造DFA
void construct_parsing_table();             // 构造分析表
void parse_input(const char* input);         // 解析输入
bool is_terminal(char symbol);               // 判断是否为终结符
void print_grammar();                        // 打印文法
void print_dfa();                            // 打印DFA
void print_parsing_table();                  // 打印分析表
void print_closure(ItemSet set, const char* prefix);  // 打印闭包

int main() {
    // setlocale(LC_ALL, "Chinese Simplified"); // 或 setlocale(LC_ALL, "zh_CN.UTF-8");

    printf("LR(0) grammar analyzer\n");
    printf("Please input the grammar (each line is a production, input empty line to end):\n");

    read_grammar();
    // print_grammar();

    extend_grammar();
    print_grammar();

    construct_dfa();
    print_dfa();

    construct_parsing_table();
    print_parsing_table();

    // char input[MAX_PROD_LEN];
    // printf("\nPlease input the string to be analyzed:");
    // scanf("%s", input);
    // parse_input(input);

    return 0;
}

// 读取文法文件并解析产生式
void read_grammar() {
    char filename[MAX_PROD_LEN];
    char full_path[MAX_PROD_LEN] = "./grammars/";
    printf("Please input the grammar file name (.txt):");
    scanf("%s", filename);
    strcat(full_path, filename);

    FILE* file = fopen(full_path, "r");
    if (file == NULL) {
        printf("Error: cannot open file %s\n", full_path);
        exit(1);
    }

    char line[MAX_PROD_LEN];
    while (fgets(line, MAX_PROD_LEN, file) != NULL) {
        // 移除换行符
        line[strcspn(line, "\n")] = 0;

        // 跳过空行
        if (strlen(line) == 0) continue;

        // 解析产生式
        char* arrow = strstr(line, "->");
        if (arrow == NULL) {
            printf("Warning: skip the line with incorrect format: %s\n", line);
            continue;
        }

        // 提取左部
        char left[MAX_PROD_LEN];
        strncpy(left, line, arrow - line);
        left[arrow - line] = '\0';

        // 提取右部并处理|符号
        char* right_part = arrow + 2;
        char* token = strtok(right_part, "|");

        while (token != NULL) {
            // 去除token前后的空格
            while (*token == ' ') token++;
            char* end = token + strlen(token) - 1;
            while (end > token && *end == ' ') *end-- = '\0';

            // 添加新的产生式
            strcpy(grammar[prod_count].left, left);
            strcpy(grammar[prod_count].right, token);
            grammar[prod_count].dot_pos = 0;
            prod_count++;

            // 获取下一个token
            token = strtok(NULL, "|");
        }
    }

    fclose(file);

    if (prod_count == 0) {
        printf("Error: no valid productions in the file\n");
        exit(1);
    }
}

// 扩展文法
void extend_grammar() {
    // 获取原始文法的开始符号（原第一个产生式的左部）
    char start_symbol[MAX_PROD_LEN];
    strcpy(start_symbol, grammar[0].left);

    // 将所有现有产生式后移一位（从后往前移动）
    for (int i = prod_count; i > 0; i--) {
        // 逐字段复制，因为结构体包含字符数组，不能直接赋值
        strcpy(grammar[i].left, grammar[i - 1].left);
        strcpy(grammar[i].right, grammar[i - 1].right);
        grammar[i].dot_pos = grammar[i - 1].dot_pos;
    }

    // 在位置0插入新的增广产生式 S' → S
    strcpy(grammar[0].left, "S'");
    strcpy(grammar[0].right, start_symbol);
    grammar[0].dot_pos = 0;

    // 更新产生式计数器
    prod_count++;
}

// 打印文法
void print_grammar() {
    printf("\nThe grammar:\n");
    for (int i = 0; i < prod_count; i++) {
        printf("%d. %s -> %s\n", i + 1, grammar[i].left, grammar[i].right);
    }
}

// 终结符判断
bool is_terminal(char symbol) {
    // 简单判断：小写字母、数字和特殊符号为终结符
    return (symbol >= 'a' && symbol <= 'z') ||
        symbol == '+' || symbol == '-' ||
        symbol == '*' || symbol == '/' ||
        symbol == '(' || symbol == ')' ||
        symbol == 'i' || symbol == 'n' ||
        (symbol >= '0' && symbol <= '9');
}

// 打印闭包
void print_closure(ItemSet set, const char* prefix) {
    printf("\n%s Item Set Colsure:\n", prefix);
    for (int i = 0; i < set.item_count; i++) {
        LR0Item item = set.items[i];
        printf("%s -> ", item.prod.left);
        for (int j = 0; j < strlen(item.prod.right); j++) {
            if (j == item.prod.dot_pos) printf("·");
            printf("%c", item.prod.right[j]);
        }
        if (item.prod.dot_pos == strlen(item.prod.right)) printf("·");
        printf("\n");
    }
}

// 计算闭包
ItemSet closure(ItemSet set) {
    ItemSet result = set;
    bool changed;
    int iteration = 0;

    do {
        changed = false;

        for (int i = 0; i < result.item_count; i++) {
            LR0Item item = result.items[i];
            if (item.prod.dot_pos < strlen(item.prod.right)) {
                char next_symbol = item.prod.right[item.prod.dot_pos];
                if (!is_terminal(next_symbol)) {
                    // 对于每个以next_symbol为左部的产生式
                    for (int j = 0; j < prod_count; j++) {
                        if (grammar[j].left[0] == next_symbol && grammar[j].left[1] == '\0') {
                            // 检查是否已存在该项目
                            bool exists = false;
                            for (int k = 0; k < result.item_count; k++) {
                                if (strcmp(result.items[k].prod.left, grammar[j].left) == 0 &&
                                    strcmp(result.items[k].prod.right, grammar[j].right) == 0 &&
                                    result.items[k].prod.dot_pos == 0) {
                                    exists = true;
                                    break;
                                }
                            }

                            if (!exists) {
                                LR0Item new_item;
                                strcpy(new_item.prod.left, grammar[j].left);
                                strcpy(new_item.prod.right, grammar[j].right);
                                new_item.prod.dot_pos = 0;
                                new_item.is_reduce = false;
                                result.items[result.item_count++] = new_item;
                                changed = true;
                                printf("Add new Item：%s -> %s\n", new_item.prod.left, new_item.prod.right);
                            }
                        }
                    }
                }
            }
        }
    } while (changed);

    //print_closure(result, "final");
    return result;
}

// 构造DFA
void construct_dfa() {
    // 初始化初始状态
    ItemSet initial_set;
    initial_set.item_count = 0;

    // 添加拓广S'->S文法为初始状态
    LR0Item initial_item;
    strcpy(initial_item.prod.left, grammar[0].left);
    strcpy(initial_item.prod.right, grammar[0].right);
    initial_item.prod.dot_pos = 0;
    initial_item.is_reduce = false;
    initial_set.items[initial_set.item_count++] = initial_item;

    // 计算初始状态的闭包，S'->S的闭包
    initial_set = closure(initial_set);
    print_closure(initial_set, "check");


    // 将初始状态添加到DFA
    dfa_states[0].item_set = initial_set;
    dfa_states[0].state_id = 0;
    state_count = 1;

    // 构造DFA
    for (int i = 0; i < state_count; i++) {
        ItemSet current_set = dfa_states[i].item_set;

        // 按符号分组：记录所有可能的转移符号
        char symbols[MAX_SYMBOLS] = { 0 };  // 所有遇到的符号
        int symbol_count = 0;

        // 收集当前状态所有可能的转移符号
        for (int j = 0; j < current_set.item_count; j++) {
            LR0Item item = current_set.items[j];
            if (item.prod.dot_pos < strlen(item.prod.right)) {
                char next_symbol = item.prod.right[item.prod.dot_pos];
                // 如果符号未记录，加入symbols
                bool exists = false;
                for (int k = 0; k < symbol_count; k++) {
                    if (symbols[k] == next_symbol) {
                        exists = true;
                        break;
                    }
                }
                if (!exists) {
                    symbols[symbol_count++] = next_symbol;
                }
            }
        }

        // 对每个符号生成转移
        for (int s = 0; s < symbol_count; s++) {
            char X = symbols[s];

            // 收集所有点号后为 X 的项目，并后移点号
            ItemSet new_set;
            new_set.item_count = 0;
            for (int j = 0; j < current_set.item_count; j++) {
                LR0Item item = current_set.items[j];
                if (item.prod.dot_pos < strlen(item.prod.right) &&
                    item.prod.right[item.prod.dot_pos] == X) {
                    LR0Item new_item = item;
                    new_item.prod.dot_pos++;
                    new_item.is_reduce = (new_item.prod.dot_pos == strlen(new_item.prod.right));
                    new_set.items[new_set.item_count++] = new_item;
                }
            }

            // 计算闭包
            new_set = closure(new_set);

            // 检查是否已存在相同状态
            int existing_state = -1;
            for (int k = 0; k < state_count; k++) {
                if (new_set.item_count == dfa_states[k].item_set.item_count) {
                    bool same = true;
                    for (int l = 0; l < new_set.item_count; l++) {
                        bool found = false;
                        for (int m = 0; m < dfa_states[k].item_set.item_count; m++) {
                            if (strcmp(new_set.items[l].prod.left, dfa_states[k].item_set.items[m].prod.left) == 0 &&
                                strcmp(new_set.items[l].prod.right, dfa_states[k].item_set.items[m].prod.right) == 0 &&
                                new_set.items[l].prod.dot_pos == dfa_states[k].item_set.items[m].prod.dot_pos) {
                                found = true;
                                break;
                            }
                        }
                        if (!found) {
                            same = false;
                            break;
                        }
                    }
                    if (same) {
                        existing_state = k;
                        break;
                    }
                }
            }

            // 添加新状态或复用已有状态
            if (existing_state == -1) {
                dfa_states[state_count].item_set = new_set;
                dfa_states[state_count].state_id = state_count;
                dfa_states[i].transitions[X] = state_count;
                state_count++;
            }
            else {
                dfa_states[i].transitions[X] = existing_state;
            }
        }
    }
}

// 打印DFA
void print_dfa() {
    printf("\nLR(0) prefix DFA:\n");
    for (int i = 0; i < state_count; i++) {
        printf("\nState %d:\n", i);
        // 打印每个状态的项目集
        for (int j = 0; j < dfa_states[i].item_set.item_count; j++) {
            // 打印左部
            LR0Item item = dfa_states[i].item_set.items[j];
            printf("%s -> ", item.prod.left);
            // 右部逐字符打印，处理 . 符号的位置
            for (int k = 0; k < strlen(item.prod.right); k++) {
                if (k == item.prod.dot_pos) printf("·");
                printf("%c", item.prod.right[k]);
            }
            if (item.prod.dot_pos == strlen(item.prod.right)) printf("·");
            printf("\n");
        }

        // 打印某个状态的状态转移
        printf("Transitions:\n");
        for (int j = 0; j < MAX_SYMBOLS; j++) {
            if (dfa_states[i].transitions[j] != 0) {
                printf("  %c -> %d\n", j, dfa_states[i].transitions[j]);
            }
        }
    }
}

// 构造分析表
void construct_parsing_table() {
    // 初始化分析表
    for (int i = 0; i < MAX_STATES; i++) {
        for (int j = 0; j < MAX_SYMBOLS; j++) {
            action_table[i][j].action = 'e';  // 错误（error）
            action_table[i][j].value = -1;
            goto_table[i][j].action = 'e';    // 错误（error）
            goto_table[i][j].value = -1;
        }
    }

    // 填充分析表
    for (int i = 0; i < state_count; i++) {
        ItemSet current_set = dfa_states[i].item_set;

        // 处理每个项目
        for (int j = 0; j < current_set.item_count; j++) {
            LR0Item item = current_set.items[j];
            // 如果是归约项目
            if (item.is_reduce) {
                // 当前项目是一个归约项目（如 A → α·）
                if (strcmp(item.prod.left, "S'") == 0) {
                    // 如果是拓广文法的初始产生式（如 S' → S·）
                    // 则在输入符号为 $（结束符）时，设置接受动作
                    action_table[i]['$'].action = 'a';  // accept
                    action_table[i]['$'].value = 0;     // 没有实际值，仅用于标识
                }
                else {
                    // 对于其他归约项目，需要找到对应的产生式编号
                    int prod_num = -1;
                    for (int k = 0; k < prod_count; k++) {
                        // 查找匹配的产生式
                        if (strcmp(grammar[k].left, item.prod.left) == 0 &&
                            strcmp(grammar[k].right, item.prod.right) == 0) {
                            prod_num = k;
                            break;
                        }
                    }

                    // 对所有终结符添加归约动作
                    for (int k = 0; k < MAX_SYMBOLS; k++) {
                        if (is_terminal(k)) {
                            action_table[i][k].action = 'r';   // reduce
                            action_table[i][k].value = prod_num; // 对应的产生式编号
                        }
                    }
                }
            }
            else {
                // 当前项目是移进项目（如 A → α·Xβ）

                // 获取点号后的符号
                char next_symbol = item.prod.right[item.prod.dot_pos];

                if (is_terminal(next_symbol)) {
                    // 如果是终结符（如 'a', '+', '(', ...）
                    action_table[i][next_symbol].action = 's'; // shift
                    action_table[i][next_symbol].value = dfa_states[i].transitions[next_symbol]; // 下一状态
                }
                else {
                    // 如果是非终结符（如 'E', 'T', 'F', ...）
                    goto_table[i][next_symbol].action = 'g'; // goto
                    goto_table[i][next_symbol].value = dfa_states[i].transitions[next_symbol]; // 下一状态
                }
            }
        }
    }
}

// 打印分析表
void print_parsing_table() {
    printf("\nLR(0) parsing table:\n");
    printf("State\t");

    // 打印终结符
    for (int i = 0; i < MAX_SYMBOLS; i++) {
        if (is_terminal(i)) {
            printf("%c\t", i);
        }
    }
    printf("|\t");

    // 打印非终结符
    for (int i = 0; i < MAX_SYMBOLS; i++) {
        if (!is_terminal(i) && i != 0) {
            printf("%c\t", i);
        }
    }
    printf("\n");

    // 打印每个状态的动作
    for (int i = 0; i < state_count; i++) {
        printf("%d\t", i);

        // 打印终结符动作
        for (int j = 0; j < MAX_SYMBOLS; j++) {
            if (is_terminal(j)) {
                if (action_table[i][j].action == 's') {
                    printf("s%d\t", action_table[i][j].value);
                }
                else if (action_table[i][j].action == 'r') {
                    printf("r%d\t", action_table[i][j].value);
                }
                else if (action_table[i][j].action == 'a') {
                    printf("acc\t");
                }
                else {
                    printf("\t");
                }
            }
        }

        printf("|\t");

        // 打印非终结符动作
        for (int j = 0; j < MAX_SYMBOLS; j++) {
            if (!is_terminal(j) && j != 0) {
                if (goto_table[i][j].action == 'g') {
                    printf("%d\t", goto_table[i][j].value);
                }
                else {
                    printf("\t");
                }
            }
        }
        printf("\n");
    }
}

// 解析输入
void parse_input(const char* input) {
    int stack[MAX_STATES];
    int stack_top = 0;
    stack[stack_top++] = 0;  // 初始状态

    int input_pos = 0;
    printf("\nParsing process:\n");
    printf("Step\tState stack\t\tInput string\t\tAction\n");

    int step = 1;
    while (1) {
        // 打印当前状态
        printf("%d\t", step++);
        for (int i = 0; i < stack_top; i++) {
            printf("%d ", stack[i]);
        }
        printf("\t\t");
        for (int i = input_pos; input[i] != '\0'; i++) {
            printf("%c", input[i]);
        }
        printf("\t\t");

        char current_symbol = input[input_pos];
        int current_state = stack[stack_top - 1];

        if (action_table[current_state][current_symbol].action == 's') {
            // 移进动作
            int next_state = action_table[current_state][current_symbol].value;
            stack[stack_top++] = next_state;
            input_pos++;
            printf("Shift %d\n", next_state);
        }
        else if (action_table[current_state][current_symbol].action == 'r') {
            // 归约动作
            int prod_num = action_table[current_state][current_symbol].value;
            int rhs_len = strlen(grammar[prod_num].right);

            // 弹出状态栈
            stack_top -= rhs_len;

            // 获取新的状态
            int new_state = goto_table[stack[stack_top - 1]][grammar[prod_num].left[0]].value;
            stack[stack_top++] = new_state;

            printf("Reduce %s -> %s\n", grammar[prod_num].left, grammar[prod_num].right);
        }
        else if (action_table[current_state][current_symbol].action == 'a') {
            // 接受动作
            printf("Accept\n");
            break;
        }
        else {
            // 错误
            printf("Error: cannot recognize the input\n");
            break;
        }
    }
}
