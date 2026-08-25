#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <locale.h>
#include <windows.h>
#define MAX_PROD_LEN 100
#define MAX_SYMBOLS 256
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

// 添加新的全局变量来存储文法中出现的符号
char terminals[MAX_SYMBOLS];    // 存储终结符
int terminal_count = 0;         // 终结符数量
char nonterminals[MAX_SYMBOLS]; // 存储非终结符
int nonterminal_count = 0;      // 非终结符数量
char follow[MAX_SYMBOLS][MAX_SYMBOLS]; // 存储每个非终结符的Follow集
char first[MAX_SYMBOLS][MAX_SYMBOLS];  // 存储每个符号的First集


// 函数声明
void read_grammar();                        // 读取文法
void extend_grammar();                      // 扩展文法
ItemSet closure(ItemSet set);               // 计算闭包
void construct_dfa();                       // 构造DFA
void construct_parsing_table();             // 构造分析表
void parse_input(const char* input);         // 分析输入串
bool is_terminal(char symbol);               // 判断是否为终结符
void print_grammar();                        // 打印文法
void print_dfa();                            // 打印DFA
void print_parsing_table();                  // 打印分析表
void print_closure(ItemSet set, const char* prefix);  // 打印闭包
void compute_follow();                      // 计算Follow集
void compute_first();
void print_follow();                        // 打印Follow集
void print_first();                         // 打印First集

// 初始化终结符和非终结符数组
void initialize_symbols() {
    // 初始化分析表
    terminal_count = 0;
    nonterminal_count = 0;

    // 遍历所有产生式
    for (int i = 0; i < prod_count; i++) {
        // 处理左部（非终结符）
        char left = grammar[i].left[0];
        bool exists = false;
        for (int j = 0; j < nonterminal_count; j++) {
            if (nonterminals[j] == left) {
                exists = true;
                break;
            }
        }
        if (!exists) {
            nonterminals[nonterminal_count++] = left;
        }

        // 处理右部
        char* right = grammar[i].right;

        // 检查是否为空串产生式
        int t = strcmp(right, "$");
        if (t == 0) {
            continue; // 空串不影响终结符/非终结符集合
        }
        // printf("%d %d %s\n", i, t, right);

        // 遍历右部每个符号
        for (int j = 0; j < strlen(right); j++) {
            char symbol = right[j];
            // printf("symbol: %c\n", symbol);

            // 排除空串符号'$'
            if (symbol == '$') continue;

            if (is_terminal(symbol)) {
                // 检查终结符是否已存在
                bool exists = false;
                for (int k = 0; k < terminal_count; k++) {
                    if (terminals[k] == symbol) {
                        exists = true;
                        break;
                    }
                }
                if (!exists) {
                    terminals[terminal_count++] = symbol;
                }
            }
            else {
                // 检查非终结符是否已存在
                bool exists = false;
                for (int k = 0; k < nonterminal_count; k++) {
                    if (nonterminals[k] == symbol) {
                        exists = true;
                        break;
                    }
                }
                if (!exists) {
                    nonterminals[nonterminal_count++] = symbol;
                }
            }
        }
    }

    // 手动添加结束符 #
    terminals[terminal_count++] = '#';
}

int main() {
    // 设置中文本地化环境
    setlocale(LC_ALL, "Chinese Simplified");  // 启用中文locale

    // 设置控制台输出为UTF-8编码
    SetConsoleOutputCP(CP_UTF8);

    // 刷新标准输出缓冲区
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("SLR(1) Parsers\n");
    printf("please enter a file name(.txt): ");

    read_grammar();

    extend_grammar();
    print_grammar();
    // 在计算Follow集之前初始化终结符和非终结符
    initialize_symbols(); // 新增函数调用

    
    printf("terminals: \n");
    for (int i = 0; i < terminal_count; i++) {
        printf("%c ", terminals[i]);
    }
    printf("\n");
    printf("nonterminals:\n");
    for (int i = 0; i < nonterminal_count; i++) {
        printf("%c ", nonterminals[i]);
    }
    printf("\n");
    


    construct_dfa();
    print_dfa();

    compute_first();
    print_first();
    compute_follow();
 
    print_follow(); // 新增：打印Follow集

    construct_parsing_table();
    print_parsing_table();

    char input[MAX_PROD_LEN];
    printf("\nplease input the str need to be anlaysis: ");
    scanf("%s", input);
    parse_input(input);

    return 0;
}

// 读取文法文件并解析产生式
void read_grammar() {
    char filename[MAX_PROD_LEN];
    char full_path[MAX_PROD_LEN] = "./grammars/";
    //printf("请输入文法文件名（.txt）：");
    scanf("%s", filename);
    strcat(full_path, filename);

    FILE* file = fopen(full_path, "r");
    if (file == NULL) {
        printf("Error: cannot open file: %s\n", full_path);
        exit(1);
    }

    char line[MAX_PROD_LEN];
    while (fgets(line, MAX_PROD_LEN, file) != NULL) {
        // 去除换行符
        line[strcspn(line, "\n")] = 0;

        // 空行处理
        if (strlen(line) == 0) continue;

        // 解析产生式格式
        char* arrow = strstr(line, "->");
        if (arrow == NULL) {
            printf("Waring: pass the wrong line: %s\n", line);
            continue;
        }

        // 提取左部
        char left[MAX_PROD_LEN];
        strncpy(left, line, arrow - line);
        left[arrow - line] = '\0';

        // 提取右部，处理|分隔的多个右部
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

            // 读取下一个token
            token = strtok(NULL, "|");
        }
    }

    fclose(file);

    if (prod_count == 0) {
        printf("Error: donot have legal parse\n");
        exit(1);
    }
}

// 扩展文法（添加S'->S产生式）
void extend_grammar() {
    // 获取原文法的开始符号（第一个产生式的左部）
    char start_symbol[MAX_PROD_LEN];
    strcpy(start_symbol, grammar[0].left);

    // 为所有产生式腾出位置，整体后移一位
    for (int i = prod_count; i > 0; i--) {
        // 逐个复制，因为是数组整体后移，不能直接赋值
        strcpy(grammar[i].left, grammar[i - 1].left);
        strcpy(grammar[i].right, grammar[i - 1].right);
        grammar[i].dot_pos = grammar[i - 1].dot_pos;
    }

    // 在位置0添加新的产生式 S' -> S
    strcpy(grammar[0].left, "S'");
    strcpy(grammar[0].right, start_symbol);
    grammar[0].dot_pos = 0;

    // 产生式数量加1
    prod_count++;
}

// 打印文法
void print_grammar() {
    printf("\nGarmmar is following:\n");
    for (int i = 0; i < prod_count; i++) {
        printf("%d. %s -> %s\n", i + 1, grammar[i].left, grammar[i].right);
    }
}

// 终结符判断
bool is_terminal(char symbol) {
    // 判断逻辑：小写字母、运算符、括号、数字等为终结符
    return (symbol >= 'a' && symbol <= 'z') ||
        symbol == '+' || symbol == '-' ||
        symbol == '*' || symbol == '/' ||
        symbol == '(' || symbol == ')' ||
        symbol == 'i' || symbol == 'n' ||
        (symbol >= '0' && symbol <= '9') ||
        symbol == '#' || symbol == '=';
}

// 打印闭包内容
void print_closure(ItemSet set, const char* prefix) {
    printf("\n%s Item Set Closure: \n", prefix);
    for (int i = 0; i < set.item_count; i++) {
        LR0Item item = set.items[i];
        printf("%s -> ", item.prod.left);
        for (int j = 0; j < strlen(item.prod.right); j++) {
            if (j == item.prod.dot_pos) printf(".");
            printf("%c", item.prod.right[j]);
        }
        if (item.prod.dot_pos == strlen(item.prod.right)) printf(".");
        printf("\n");
    }
}

// 计算项目集的闭包
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
                    // 对每个以next_symbol为左部的产生式
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
                                // printf("Add new Item: %s -> %s\n", new_item.prod.left, new_item.prod.right);
                            }
                        }
                    }
                }
            }
        }
    } while (changed);

    // print_closure(result, "最终");
    return result;
}

// 构造活前缀DFA
void construct_dfa() {
    // 初始化初始状态
    ItemSet initial_set;
    initial_set.item_count = 0;

    // 添加S'->S产生式作为初始项目
    LR0Item initial_item;
    strcpy(initial_item.prod.left, grammar[0].left);
    strcpy(initial_item.prod.right, grammar[0].right);
    initial_item.prod.dot_pos = 0;
    initial_item.is_reduce = false;
    initial_set.items[initial_set.item_count++] = initial_item;

    // 计算初始状态的闭包（即S'->S的闭包）
    initial_set = closure(initial_set);
    // print_closure(initial_set, "check");


    // 将初始状态添加到DFA中
    dfa_states[0].item_set = initial_set;
    dfa_states[0].state_id = 0;
    state_count = 1;

    // 构造DFA
    for (int i = 0; i < state_count; i++) {
        ItemSet current_set = dfa_states[i].item_set;

        // 收集符号：记录所有可能的转移符号
        char symbols[MAX_SYMBOLS] = { 0 };  // 存储符号集合
        int symbol_count = 0;

        // 遍历当前状态的所有项目，收集可转移的符号
        for (int j = 0; j < current_set.item_count; j++) {
            LR0Item item = current_set.items[j];
            if (item.prod.dot_pos < strlen(item.prod.right)) {
                char next_symbol = item.prod.right[item.prod.dot_pos];
                // 检查符号是否已记录在symbols中
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

        // 对每个符号进行状态转移
        for (int s = 0; s < symbol_count; s++) {
            char X = symbols[s];

            // 收集当前项目集中点后为X的项目，生成新的项目集
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

            // 计算新状态的闭包
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

            // 如果是新状态，添加到DFA中；否则使用已存在的状态
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


// 判断是否为接受状态（包含 S' -> S. 的项目）
int is_accept_state(ItemSet* item_set) {
    for (int i = 0; i < item_set->item_count; i++) {
        LR0Item item = item_set->items[i];
        if (item.prod.left == 'S' &&
            strcmp(item.prod.right, "S") == 0 &&
            item.prod.dot_pos == strlen(item.prod.right)) {
            return 1;
        }
    }
    return 0;
}

// 保存DFA为JSON格式
void save_dfa_to_json(const char* filename) {
    FILE* fp = fopen(filename, "w");
    if (!fp) {
        perror("无法打开文件");
        return;
    }

    int accept_states[MAX_STATES];
    int accept_count = 0;

    // 收集接受状态
    for (int i = 0; i < state_count; i++) {
        if (is_accept_state(&dfa_states[i].item_set)) {
            accept_states[accept_count++] = i;
        }
    }

    // 开始写入JSON
    fprintf(fp, "{\n");
    fprintf(fp, "  \"start_state\": 0,\n");

    // 写入接受状态
    fprintf(fp, "  \"accept_states\": [");
    for (int i = 0; i < accept_count; i++) {
        fprintf(fp, "%d", accept_states[i]);
        if (i < accept_count - 1) {
            fprintf(fp, ", ");
        }
    }
    fprintf(fp, "],\n");

    // 写入状态列表
    fprintf(fp, "  \"states\": [\n");
    for (int i = 0; i < state_count; i++) {
        fprintf(fp, "    {\n");
        fprintf(fp, "      \"id\": %d,\n", i);

        // 写入项目集
        fprintf(fp, "      \"items\": [\n");
        for (int j = 0; j < dfa_states[i].item_set.item_count; j++) {
            LR0Item item = dfa_states[i].item_set.items[j];
            fprintf(fp, "        \"%s -> ", item.prod.left);
            for (int k = 0; k < strlen(item.prod.right); k++) {
                if (k == item.prod.dot_pos) fprintf(fp, ".");
                fprintf(fp, "%c", item.prod.right[k]);
            }
            if (item.prod.dot_pos == strlen(item.prod.right)) fprintf(fp, ".");
            fprintf(fp, "\"");
            if (j < dfa_states[i].item_set.item_count - 1) {
                fprintf(fp, ",");
            }
            fprintf(fp, "\n");
        }
        fprintf(fp, "      ],\n");

        // 写入转移函数
        fprintf(fp, "      \"transitions\": {\n");
        int trans_count = 0;
        for (int j = 0; j < MAX_SYMBOLS; j++) {
            if (dfa_states[i].transitions[j] != 0) {
                if (trans_count > 0) fprintf(fp, ",\n");
                fprintf(fp, "        \"%c\": %d", (char)j, dfa_states[i].transitions[j]);
                trans_count++;
            }
        }
        fprintf(fp, "\n      }\n");
        fprintf(fp, "    }");
        if (i < state_count - 1) fprintf(fp, ",");
        fprintf(fp, "\n");
    }
    fprintf(fp, "  ]\n");
    fprintf(fp, "}\n");

    fclose(fp);
    printf("DFA已保存到 %s\n", filename);
}

// 原有打印DFA函数
void print_dfa() {
    printf("\nLR(0) active DFA: \n");
    for (int i = 0; i < state_count; i++) {
        printf("\nstate %d: \n", i);
        for (int j = 0; j < dfa_states[i].item_set.item_count; j++) {
            LR0Item item = dfa_states[i].item_set.items[j];
            printf("\t%s -> ", item.prod.left);
            for (int k = 0; k < strlen(item.prod.right); k++) {
                if (k == item.prod.dot_pos) printf(".");
                printf("%c", item.prod.right[k]);
            }
            if (item.prod.dot_pos == strlen(item.prod.right)) printf(".");
            printf("\n");
        }

        printf("  transition: \n");
        for (int j = 0; j < MAX_SYMBOLS; j++) {
            if (dfa_states[i].transitions[j] != 0) {
                printf("\t%c -> %d\n", j, dfa_states[i].transitions[j]);
            }
        }
    }

    // 新增功能：保存为JSON文件
    save_dfa_to_json("dfa_slr1.json");
}

// 计算First集
void compute_first() {
    // 初始化First集
    for (int i = 0; i < MAX_SYMBOLS; i++) {
        memset(first[i], 0, MAX_SYMBOLS);
    }

    // 终结符的First集是其自身
    for (int i = 0; i < terminal_count; i++) {
        char symbol = terminals[i];
        first[(int)symbol][(int)symbol] = 1;
    }
    bool changed;
    do {
        changed = false;
        for (int i = 0; i < prod_count; i++) {
            char left = grammar[i].left[0];
            char* right = grammar[i].right;

            // 处理空产生式
            if (strcmp(right, "$") == 0) {
                if (!first[(int)left][(int)'$']) {
                    first[(int)left][(int)'$'] = 1;
                    changed = true;
                }
                continue;
            }
            // 若右部首个符号是终结符，直接加入左部符号的First集
            char first_symbol = right[0];
            if (is_terminal(first_symbol)) {
                if (!first[(int)left][(int)first_symbol]) {
                    first[(int)left][(int)first_symbol] = 1;
                    changed = true;
                }
            }
            // 处理非空产生式
            bool all_epsilon = true;
            for (int j = 0; right[j] != '\0'; j++) {
                char symbol = right[j];
                // 将First(symbol)中除ε外的所有元素添加到First(left)
                for (int k = 0; k < MAX_SYMBOLS; k++) {
                    if (first[(int)symbol][k] && k != (int)'$') {
                        if (!first[(int)left][k]) {
                            first[(int)left][k] = 1;
                            changed = true;
                        }
                    }
                }
                // 如果当前符号不能推导出ε，则后续符号不再处理
                if (!first[(int)symbol][(int)'$']) {
                    all_epsilon = false;
                    break;
                }
            }
            // 如果所有符号都能推导出ε，则left的First集包含ε
            if (all_epsilon) {
                if (!first[(int)left][(int)'$']) {
                    first[(int)left][(int)'$'] = 1;
                    changed = true;
                }
            }
        }
    } while (changed);
}

// 计算Follow集
void compute_follow() {
    // 初始化Follow集
    for (int i = 0; i < nonterminal_count; i++) {
        memset(follow[i], 0, MAX_SYMBOLS);
    }

    // 将#加入到开始符号S'的Follow集中
    for (int i = 0; i < nonterminal_count; i++) {
        if (nonterminals[i] == 'S' && i == 0) { // 假设S'是第一个非终结符
            follow[i][(int)'#'] = 1;
            break;
        }
    }

    bool changed;
    do {
        changed = false;
        for (int i = 0; i < prod_count; i++) {
            char* left = grammar[i].left;
            char* right = grammar[i].right;
            int len = strlen(right);
            for (int j = 0; j < len; j++) {
                char symbol = right[j];
                if (!is_terminal(symbol)) {
                    int B_index = -1;
                    for (int k = 0; k < nonterminal_count; k++) {
                        if (nonterminals[k] == symbol) {
                            B_index = k;
                            break;
                        }
                    }
                    if (B_index == -1) continue;
                    // 处理 A → αBβ 的情况
                    if (j < len - 1) {
                        char* beta = &right[j + 1];
                        // 将First(β)中除ε外的所有符号加入Follow(B)
                        for (int k = 0; beta[k] != '\0'; k++) {
                            char beta_symbol = beta[k];
                            for (int m = 0; m < MAX_SYMBOLS; m++) {
                                if (first[(int)beta_symbol][m] && m != (int)'$') {
                                    if (!follow[B_index][m]) {
                                        follow[B_index][m] = 1;
                                        changed = true;
                                    }
                                }
                            }
                            // 如果当前符号不能推导出ε，则停止处理后续符号
                            if (!first[(int)beta_symbol][(int)'$']) {
                                break;
                            }
                        }
                        // 如果β能推导出ε，则将Follow(A)加入Follow(B)
                        bool all_epsilon = true;
                        for (int k = 0; beta[k] != '\0'; k++) {
                            if (!first[(int)beta[k]][(int)'$']) {
                                all_epsilon = false;
                                break;
                            }
                        }
                        if (all_epsilon) {
                            int A_index = -1;
                            for (int k = 0; k < nonterminal_count; k++) {
                                if (nonterminals[k] == left[0]) {
                                    A_index = k;
                                    break;
                                }
                            }
                            if (A_index != -1) {
                                for (int k = 0; k < MAX_SYMBOLS; k++) {
                                    if (follow[A_index][k] && !follow[B_index][k]) {
                                        follow[B_index][k] = 1;
                                        changed = true;
                                    }
                                }
                            }
                        }
                    }
                    // 处理 A → αB 的情况（即β为空）
                    if (j == len - 1) {
                        int A_index = -1;
                        for (int k = 0; k < nonterminal_count; k++) {
                            if (nonterminals[k] == left[0]) {
                                A_index = k;
                                break;
                            }
                        }
                        if (A_index != -1) {
                            for (int k = 0; k < MAX_SYMBOLS; k++) {
                                if (follow[A_index][k] && !follow[B_index][k]) {
                                    follow[B_index][k] = 1;
                                    changed = true;
                                }
                            }
                        }
                    }
                }
            }
        }
    } while (changed);
}



// 构造SLR(1)分析表
void construct_parsing_table() {
    // 初始化分析表
    for (int i = 0; i < MAX_STATES; i++) {
        for (int j = 0; j < MAX_SYMBOLS; j++) {
            action_table[i][j].action = 'e';  // 表示错误
            action_table[i][j].value = -1;
            goto_table[i][j].action = 'e';    // 表示错误
            goto_table[i][j].value = -1;
        }
    }

    // 构造分析表
    for (int i = 0; i < state_count; i++) {
        ItemSet current_set = dfa_states[i].item_set;

        // 处理每个项目
        for (int j = 0; j < current_set.item_count; j++) {
            LR0Item item = current_set.items[j];
            // 如果是归约项目
            if (item.is_reduce) {
                if (strcmp(item.prod.left, "S'") == 0) {
                    action_table[i]['#'].action = 'a';  // 接受
                    action_table[i]['#'].value = 0;
                }
                else {
                    // 找到对应的产生式编号
                    int prod_num = -1;
                    for (int k = 0; k < prod_count; k++) {
                        if (strcmp(grammar[k].left, item.prod.left) == 0 &&
                            strcmp(grammar[k].right, item.prod.right) == 0) {
                            prod_num = k;
                            break;
                        }
                    }

                    // 找到左部非终结符的Follow集
                    int nonterminal_index = -1;
                    for (int k = 0; k < nonterminal_count; k++) {
                        if (nonterminals[k] == item.prod.left[0]) {
                            nonterminal_index = k;
                            break;
                        }
                    }

                    if (nonterminal_index != -1) {
                        // 只对Follow集中的终结符添加归约动作
                        for (int k = 0; k < MAX_SYMBOLS; k++) {
                            if (follow[nonterminal_index][k] && is_terminal((char)k)) {
                                action_table[i][k].action = 'r';
                                action_table[i][k].value = prod_num;
                            }
                        }
                    }
                }
            }
            else {
                // 当前项目是移进项目
                char next_symbol = item.prod.right[item.prod.dot_pos];

                if (is_terminal(next_symbol)) {
                    action_table[i][next_symbol].action = 's';
                    action_table[i][next_symbol].value = dfa_states[i].transitions[next_symbol];
                }
                else {
                    goto_table[i][next_symbol].action = 'g';
                    goto_table[i][next_symbol].value = dfa_states[i].transitions[next_symbol];
                }
            }
        }
    }
}

// 打印分析表
void print_parsing_table() {
    printf("\nSLR(1) Analysis Table: \n");
    printf("state\t");

    // 打印终结符列标题
    for (int i = 0; i < terminal_count; i++) {
        printf("%c\t", terminals[i]);
    }
    printf("|\t");

    // 打印非终结符列标题
    for (int i = 0; i < nonterminal_count; i++) {
        // 正确过滤S'，而不是S
        if (nonterminals[i] != 'S' || i != 0) {  // 假设S'是第一个非终结符
            printf("%c\t", nonterminals[i]);
        }
    }
    printf("\n");

    // 打印每个状态的动作
    for (int i = 0; i < state_count; i++) {
        printf("%d\t", i);

        // 打印终结符对应的动作
        for (int j = 0; j < terminal_count; j++) {
            char symbol = terminals[j];
            if (action_table[i][symbol].action == 's') {
                printf("s%d\t", action_table[i][symbol].value);
            }
            else if (action_table[i][symbol].action == 'r') {
                printf("r%d\t", action_table[i][symbol].value);
            }
            else if (action_table[i][symbol].action == 'a') {
                printf("acc\t");
            }
            else {
                printf("\t");
            }
        }

        printf("|\t");

        // 打印非终结符对应的goto
        for (int j = 0; j < nonterminal_count; j++) {
            char symbol = nonterminals[j];
            // 正确过滤S'，而不是S
            if (symbol != 'S' || j != 0) {  // 假设S'是第一个非终结符
                if (goto_table[i][symbol].action == 'g') {
                    printf("%d\t", goto_table[i][symbol].value);
                }
                else {
                    printf("\t");
                }
            }
        }
        printf("\n");
    }
}

// 基于SLR(1)分析表的语法分析过程
void parse_input(const char* input) {
    int stack[MAX_STATES];  // 状态栈
    char char_stack[MAX_STATES];  // 字符栈
    int stack_top = 0;
    stack[stack_top++] = 0;  // 初始状态入栈
    char_stack[stack_top - 1] = '#';  // 假设初始符号为#，表示栈底

    int input_pos = 0;
    char input_with_end[MAX_PROD_LEN];
    strcpy(input_with_end, input);
    strcat(input_with_end, "#");  // 添加结束符#

    printf("\ngramar analysis processing: \n");
    printf("step\tstate stack\t\tinput str.\t\taction\n");

    int step = 1;
    while (1) {
        // 打印当前状态
        printf("%d\t", step++);
        for (int i = 0; i < stack_top; i++) {
            printf("%d ", stack[i]);
        }

        printf("\n\t");
        for (int i = 0; i < stack_top; i++) {
            printf("%c ", char_stack[i]);
        }
        printf("\t\t\t");
        for (int i = input_pos; input_with_end[i] != '\0'; i++) {
            printf("%c", input_with_end[i]);
        }
        //printf("\n");

        char current_symbol = input_with_end[input_pos];
        int current_state = stack[stack_top - 1];

        if (action_table[current_state][current_symbol].action == 's') {
            // 移进操作
            int next_state = action_table[current_state][current_symbol].value;
            stack[stack_top++] = next_state;
            char_stack[stack_top - 1] = current_symbol;  // 将当前符号压入字符栈
            input_pos++;
            printf("\t\tshift %d\n", next_state);
        }
        else if (action_table[current_state][current_symbol].action == 'r') {
            // 归约操作
            int prod_num = action_table[current_state][current_symbol].value;
            int rhs_len = strlen(grammar[prod_num].right);

            // 弹出右部长度的状态和字符
            stack_top -= rhs_len;
            for (int i = 0; i < rhs_len; i++) {
                char_stack[stack_top + i] = '\0';  // 清除弹出的字符
            }

            // 获取新状态
            int new_state = goto_table[stack[stack_top - 1]][grammar[prod_num].left[0]].value;
            stack[stack_top++] = new_state;
            char_stack[stack_top - 1] = grammar[prod_num].left[0];  // 将归约后的非终结符压入字符栈

            printf("\t\treduce %s -> %s\n", grammar[prod_num].left, grammar[prod_num].right);
        }
        else if (action_table[current_state][current_symbol].action == 'a') {
            // 接受操作
            printf("\t\taccept\n");
            break;
        }
        else {
            // 分析错误
            printf("\t\tError: The input string cannot be reduced to the start symbol.\n");
            break;
        }
    }
}

// 打印Follow集
void print_follow() {
    printf("\nFollow Sets:\n");
    for (int i = 0; i < nonterminal_count; i++) {
        printf("Follow(%c) = { ", nonterminals[i]);
        bool first = true;
        for (int j = 0; j < MAX_SYMBOLS; j++) {
            if (follow[i][j]) {
                if (!first) {
                    printf(", ");
                }
                printf("%c", (char)j);
                first = false;
            }
        }
        printf(" }\n");
    }
}

// 打印First集合
void print_first() {
    printf("\nFirst集合:\n");

    // 打印非终结符的First集
    for (int i = 0; i < nonterminal_count; i++) {
        char symbol = nonterminals[i];
        printf("First(%c) = { ", symbol);

        bool firstElement = true;
        for (int j = 0; j < MAX_SYMBOLS; j++) {
            if (first[(int)symbol][j]) {
                if (!firstElement) {
                    printf(", ");
                }
                if (j == (int)'$') {
                    printf("$");
                }
                else {
                    printf("%c", (char)j);
                }
                firstElement = false;
            }
        }

        printf(" }\n");
    }

    // 打印终结符的First集
    printf("\n终结符的First集:\n");
    for (int i = 0; i < terminal_count; i++) {
        char symbol = terminals[i];
        printf("First(%c) = { %c }\n", symbol, symbol);
    }
}