#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <locale.h>
#include <windows.h>
#define MAX_PROD_LEN 100
#define MAX_SYMBOLS 256
#define MAX_STATES 200 // 增加状态数，LR(1)状态可能更多
#define MAX_ITEMS 200  // 增加项目数
#define MAX_LOOKAHEAD 10 // 定义MAX_LOOKAHEAD

// 产生式结构
typedef struct {
    char left[MAX_PROD_LEN];    // 左部
    char right[MAX_PROD_LEN];   // 右部
    int dot_pos;                // 点的位置
} Production;

// LR(1)项目结构
typedef struct {
    Production prod;
    char lookahead;             // 展望符号
    bool is_reduce;             // 是否为归约项目
} LR1Item;

// 项目集结构
typedef struct {
    LR1Item items[MAX_ITEMS];
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

char terminals[MAX_SYMBOLS];    // 存储终结符
int terminal_count = 0;         // 终结符数量
char nonterminals[MAX_SYMBOLS]; // 存储非终结符
int nonterminal_count = 0;      // 非终结符数量

// FIRST集
char first[MAX_SYMBOLS][MAX_SYMBOLS]; // first[i][c] = 1表示nonterminals[i]的FIRST集包含c

// 函数声明
void read_grammar();
void extend_grammar();
ItemSet closure(ItemSet set);
void construct_dfa();
void construct_parsing_table();
void parse_input(const char* input);
bool is_terminal(char symbol);
void print_grammar();
void print_dfa();
void print_parsing_table();
void print_closure(ItemSet set, const char* prefix);
void initialize_symbols(); // 声明initialize_symbols

// 新增LR(1)辅助函数声明
int get_first_set(char X, char* first_set);
void compute_first();
bool lr1item_equal(LR1Item* a, LR1Item* b);
bool itemset_equal(ItemSet* a, ItemSet* b);
ItemSet goto_lr1(ItemSet set, char X);

int main() {
    // 设置中文本地化环境
    setlocale(LC_ALL, "Chinese Simplified");
    SetConsoleOutputCP(CP_UTF8);
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("LR(1) Parser\n");
    printf("please enter a file name(.txt): ");

    read_grammar();
    extend_grammar();
    print_grammar();

    // 初始化符号，并计算FIRST集
    initialize_symbols();
    compute_first();

    construct_dfa();
    print_dfa();

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
    scanf("%s", filename);
    strcat(full_path, filename);

    FILE* file = fopen(full_path, "r");
    if (file == NULL) {
        printf("Error: cannot open file: %s\n", full_path);
        exit(1);
    }

    char line[MAX_PROD_LEN];
    while (fgets(line, MAX_PROD_LEN, file) != NULL) {
        line[strcspn(line, "\n")] = 0;
        if (strlen(line) == 0) continue;

        char* arrow = strstr(line, "->");
        if (arrow == NULL) {
            printf("Warning: skip error line: %s\n", line);
            continue;
        }

        char left[MAX_PROD_LEN];
        int left_len = arrow - line;
        strncpy(left, line, left_len);
        left[left_len] = '\0';

        // 去除左部前后空格
        char* left_trim = left;
        while (*left_trim == ' ') left_trim++;
        char* left_end = left_trim + strlen(left_trim) - 1;
        while (left_end > left_trim && *left_end == ' ') *left_end-- = '\0';

        char* right_part = arrow + 2;
        char* token = strtok(right_part, "|");

        while (token != NULL) {
            while (*token == ' ') token++;
            char* end = token + strlen(token) - 1;
            while (end > token && *end == ' ') *end-- = '\0';

            strcpy(grammar[prod_count].left, left_trim);
            strcpy(grammar[prod_count].right, token);
            grammar[prod_count].dot_pos = 0;
            prod_count++;

            token = strtok(NULL, "|");
        }
    }

    fclose(file);

    if (prod_count == 0) {
        printf("Error: no valid productions found\n");
        exit(1);
    }
}

// 扩展文法（添加S'->S产生式）
void extend_grammar() {
    char start_symbol[MAX_PROD_LEN];
    strcpy(start_symbol, grammar[0].left);

    // 去除start_symbol前后空格
    char* start_trim = start_symbol;
    while (*start_trim == ' ') start_trim++;
    char* start_end = start_trim + strlen(start_trim) - 1;
    while (start_end > start_trim && *start_end == ' ') *start_end-- = '\0';

    for (int i = prod_count; i > 0; i--) {
        strcpy(grammar[i].left, grammar[i - 1].left);
        strcpy(grammar[i].right, grammar[i - 1].right);
        grammar[i].dot_pos = grammar[i - 1].dot_pos;
    }

    strcpy(grammar[0].left, "S'");
    strcpy(grammar[0].right, start_trim);
    grammar[0].dot_pos = 0;

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
    return (symbol >= 'a' && symbol <= 'z') ||
        symbol == '+' || symbol == '-' ||
        symbol == '*' || symbol == '/' ||
        symbol == '(' || symbol == ')' ||
        symbol == 'i' || symbol == 'n' ||
        (symbol >= '0' && symbol <= '9') ||
        symbol == '#' || symbol == '='; // 添加=
}

// 初始化终结符和非终结符数组
void initialize_symbols() {
    terminal_count = 0;
    nonterminal_count = 0;

    // 遍历所有产生式
    for (int i = 0; i < prod_count; i++) {
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
        for (int j = 0; j < strlen(grammar[i].right); j++) {
            char symbol = grammar[i].right[j];
            if (is_terminal(symbol)) {
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

// 计算符号X的FIRST集，结果存入first_set，返回数量
int get_first_set(char X, char* first_set) {
    int count = 0;
    if (is_terminal(X)) {
        first_set[count++] = X;
        return count;
    }

    int idx = -1;
    for (int i = 0; i < nonterminal_count; i++) {
        if (nonterminals[i] == X) { idx = i; break; }
    }
    if (idx == -1) return 0; // 未知非终结符，这不应该发生

    for (int c = 0; c < MAX_SYMBOLS; c++) {
        if (first[idx][c]) first_set[count++] = (char)c;
    }
    return count;
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

// 判断两个LR1Item是否相等
bool lr1item_equal(LR1Item* a, LR1Item* b) {
    return strcmp(a->prod.left, b->prod.left) == 0 &&
           strcmp(a->prod.right, b->prod.right) == 0 &&
           a->prod.dot_pos == b->prod.dot_pos &&
           a->lookahead == b->lookahead;
}

// 判断两个项目集是否相等
bool itemset_equal(ItemSet* a, ItemSet* b) {
    if (a->item_count != b->item_count) return false;
    for (int i = 0; i < a->item_count; i++) {
        bool found = false;
        for (int j = 0; j < b->item_count; j++) {
            if (lr1item_equal(&a->items[i], &b->items[j])) {
                found = true; break;
            }
        }
        if (!found) return false;
    }
    return true;
}

// LR(1) goto操作：对项目集I和符号X，返回GOTO(I, X)
ItemSet goto_lr1(ItemSet set, char X) {
    ItemSet new_set;
    new_set.item_count = 0;
    for (int i = 0; i < set.item_count; i++) {
        LR1Item item = set.items[i];
        int right_len = strlen(item.prod.right);
        if (item.prod.dot_pos < right_len && item.prod.right[item.prod.dot_pos] == X) {
            LR1Item moved = item;
            moved.prod.dot_pos++;
            moved.is_reduce = (moved.prod.dot_pos == strlen(moved.prod.right));
            new_set.items[new_set.item_count++] = moved;
        }
    }
    return closure(new_set);
}

// LR(1)项目集闭包
ItemSet closure(ItemSet set) {
    ItemSet result = set;
    bool changed;
    do {
        changed = false;
        for (int i = 0; i < result.item_count; i++) {
            LR1Item item = result.items[i];
            int right_len = strlen(item.prod.right);
            if (item.prod.dot_pos < right_len) {
                char B = item.prod.right[item.prod.dot_pos];
                if (!is_terminal(B)) {
                    // 计算beta a
                    char beta_a_str[MAX_PROD_LEN + MAX_LOOKAHEAD + 1] = {0};
                    int beta_a_len = 0;
                    // beta
                    for (int k = item.prod.dot_pos + 1; k < right_len; k++) {
                        beta_a_str[beta_a_len++] = item.prod.right[k];
                    }
                    // a (lookahead)
                    beta_a_str[beta_a_len++] = item.lookahead;
                    beta_a_str[beta_a_len] = '\0';

                    // 计算FIRST(beta a)
                    char first_set[MAX_SYMBOLS] = {0};
                    int first_count = 0;

                    // 遍历beta a中的每个符号，收集FIRST集
                    for (int k = 0; k < beta_a_len; k++) {
                        char current_symbol = beta_a_str[k];
                        char temp_first[MAX_SYMBOLS] = {0};
                        int temp_count = get_first_set(current_symbol, temp_first);
                        bool has_epsilon = false; // 假设FIRST集不包含ε，简化处理

                        for (int c = 0; c < temp_count; c++) {
                            if (!first_set[(int)temp_first[c]]) { // 避免重复添加
                                first_set[first_count++] = temp_first[c];
                            }
                        }
                        // 如果当前符号不能推导出ε，则停止遍历
                        if (!has_epsilon) break;
                    }

                    // 对每个B->gamma，添加[B->.gamma, x]到闭包
                    for (int j = 0; j < prod_count; j++) {
                        if (grammar[j].left[0] == B && grammar[j].left[1] == '\0') {
                            for (int f = 0; f < first_count; f++) {
                                LR1Item new_item;
                                strcpy(new_item.prod.left, grammar[j].left);
                                strcpy(new_item.prod.right, grammar[j].right);
                                new_item.prod.dot_pos = 0;
                                new_item.lookahead = first_set[f];
                                new_item.is_reduce = (strlen(new_item.prod.right) == 0); // ε产生式
                                // 检查是否已存在该项目
                                bool exists = false;
                                for (int m = 0; m < result.item_count; m++) {
                                    if (lr1item_equal(&result.items[m], &new_item)) {
                                        exists = true; break;
                                    }
                                }
                                if (!exists) {
                                    result.items[result.item_count++] = new_item;
                                    changed = true;
                                }
                            }
                        }
                    }
                }
            }
        }
    } while (changed);
    return result;
}

// 构造LR(1) DFA（项目集族）
void construct_dfa() {
    ItemSet initial_set;
    initial_set.item_count = 0;
    LR1Item initial_item;
    strcpy(initial_item.prod.left, grammar[0].left);
    strcpy(initial_item.prod.right, grammar[0].right);
    initial_item.prod.dot_pos = 0;
    initial_item.lookahead = '#'; // 初始展望符为#
    initial_item.is_reduce = false;
    initial_set.items[initial_set.item_count++] = initial_item;

    initial_set = closure(initial_set);
    dfa_states[0].item_set = initial_set;
    dfa_states[0].state_id = 0;
    state_count = 1;

    for (int i = 0; i < state_count; i++) {
        ItemSet current_set = dfa_states[i].item_set;
        char symbols_to_process[MAX_SYMBOLS] = {0};
        int symbols_count = 0;

        for (int j = 0; j < current_set.item_count; j++) {
            LR1Item item = current_set.items[j];
            if (item.prod.dot_pos < strlen(item.prod.right)) {
                char next_symbol = item.prod.right[item.prod.dot_pos];
                bool exists = false;
                for (int k = 0; k < symbols_count; k++) {
                    if (symbols_to_process[k] == next_symbol) { exists = true; break; }
                }
                if (!exists) { symbols_to_process[symbols_count++] = next_symbol; }
            }
        }

        for (int s = 0; s < symbols_count; s++) {
            char X = symbols_to_process[s];
            ItemSet next_set = goto_lr1(current_set, X);

            if (next_set.item_count == 0) continue; // 空的goto集合

            int existing_state = -1;
            for (int k = 0; k < state_count; k++) {
                if (itemset_equal(&dfa_states[k].item_set, &next_set)) {
                    existing_state = k; break;
                }
            }

            if (existing_state == -1) {
                if (state_count >= MAX_STATES) { // 检查数组边界
                    printf("Error: Max states reached. Increase MAX_STATES.\n");
                    exit(1);
                }
                dfa_states[state_count].item_set = next_set;
                dfa_states[state_count].state_id = state_count;
                dfa_states[i].transitions[(int)X] = state_count; // Cast to int for array index
                state_count++;
            } else {
                dfa_states[i].transitions[(int)X] = existing_state;
            }
        }
    }
}


// 判断是否为接受状态（包含 S' -> S., [#]）
int is_accept_state(ItemSet* item_set) {
    for (int i = 0; i < item_set->item_count; i++) {
        LR1Item item = item_set->items[i];
        // 直接比较 char 和字符常量（隐式转换为 int）
        if (item.prod.left == 'S' && 
            strcmp(item.prod.right, "S") == 0 && 
            item.prod.dot_pos == strlen(item.prod.right) &&
            item.lookahead == '#') {
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
            LR1Item item = dfa_states[i].item_set.items[j];
            fprintf(fp, "        \"%s -> ", item.prod.left);
            // if (item.prod.left == '\0') {
            //     fprintf(fp, "        \" -> ");
            // } else {
            //     fprintf(fp, "        \"%c -> ", item.prod.left);
            // }

            for (int k = 0; k < strlen(item.prod.right); k++) {
                if (k == item.prod.dot_pos) fprintf(fp, ".");
                fprintf(fp, "%c", item.prod.right[k]);
            }
            if (item.prod.dot_pos == strlen(item.prod.right)) fprintf(fp, ".");
            fprintf(fp, ", [%c]\"", item.lookahead);
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

// 打印DFA
void print_dfa() {
    printf("\nLR(1) DFA (Item Sets): \n");
    for (int i = 0; i < state_count; i++) {
        printf("\nState %d: \n", i);
        for (int j = 0; j < dfa_states[i].item_set.item_count; j++) {
            LR1Item item = dfa_states[i].item_set.items[j];
            printf("\t%s -> ", item.prod.left);
            // if (item.prod.left == '\0') {
            //     printf("\t -> ");
            // } else {
            //     printf("\t%c -> ", item.prod.left);
            // }

            for (int k = 0; k < strlen(item.prod.right); k++) {
                if (k == item.prod.dot_pos) printf(".");
                printf("%c", item.prod.right[k]);
            }
            if (item.prod.dot_pos == strlen(item.prod.right)) printf(".");
            printf(", [%c]\n", item.lookahead);
        }

        printf("  Transitions: \n");
        for (int j = 0; j < MAX_SYMBOLS; j++) {
            if (dfa_states[i].transitions[j] != 0) {
                printf("\t%c -> %d\n", (char)j, dfa_states[i].transitions[j]);
            }
        }
    }

    // 新增：保存为JSON文件
    save_dfa_to_json("dfa_LR1.json");
}

// 构造LR(1)分析表
void construct_parsing_table() {
    for (int i = 0; i < MAX_STATES; i++) {
        for (int j = 0; j < MAX_SYMBOLS; j++) {
            action_table[i][j].action = 'e'; // Error
            action_table[i][j].value = -1;
            goto_table[i][j].action = 'e';   // Error
            goto_table[i][j].value = -1;
        }
    }

    for (int i = 0; i < state_count; i++) {
        ItemSet current_set = dfa_states[i].item_set;

        for (int j = 0; j < current_set.item_count; j++) {
            LR1Item item = current_set.items[j];

            // 移进项
            if (item.prod.dot_pos < strlen(item.prod.right)) {
                char next_symbol = item.prod.right[item.prod.dot_pos];
                if (is_terminal(next_symbol)) {
                    int next_state = dfa_states[i].transitions[(int)next_symbol];
                    if (action_table[i][(int)next_symbol].action != 'e' && 
                        (action_table[i][(int)next_symbol].action != 's' || action_table[i][(int)next_symbol].value != next_state)) {
                        printf("Conflict detected at state %d, symbol %c: existing %c%d, new s%d\n",
                                i, next_symbol, action_table[i][(int)next_symbol].action, action_table[i][(int)next_symbol].value, next_state);
                        // 优先移进，LR(1)应该不会有S/R冲突
                    }
                    action_table[i][(int)next_symbol].action = 's';
                    action_table[i][(int)next_symbol].value = next_state;
                } else { // 非终结符，填充GOTO表
                    int next_state = dfa_states[i].transitions[(int)next_symbol];
                    if (goto_table[i][(int)next_symbol].action != 'e' && 
                        (goto_table[i][(int)next_symbol].action != 'g' || goto_table[i][(int)next_symbol].value != next_state)) {
                        printf("Conflict detected at GOTO table state %d, symbol %c: existing g%d, new g%d\n",
                                i, next_symbol, goto_table[i][(int)next_symbol].value, next_state);
                    }
                    goto_table[i][(int)next_symbol].action = 'g';
                    goto_table[i][(int)next_symbol].value = next_state;
                }
            } else { // 归约项 A -> α.
                if (strcmp(item.prod.left, "S'") == 0 && item.lookahead == '#') {
                    // 接受项 S' -> S. , #
                    if (action_table[i][(int)item.lookahead].action != 'e' && 
                        (action_table[i][(int)item.lookahead].action != 'a')) {
                        printf("Conflict detected at state %d, symbol %c: existing %c%d, new acc\n",
                                i, item.lookahead, action_table[i][(int)item.lookahead].action, action_table[i][(int)item.lookahead].value);
                    }
                    action_table[i][(int)item.lookahead].action = 'a';
                    action_table[i][(int)item.lookahead].value = 0; // Convention for accept
                } else {
                    // 归约项 A -> α. , a
                    int prod_num = -1;
                    for (int k = 0; k < prod_count; k++) {
                        if (strcmp(grammar[k].left, item.prod.left) == 0 &&
                            strcmp(grammar[k].right, item.prod.right) == 0) {
                            prod_num = k;
                            break;
                        }
                    }
                    if (prod_num == -1) { // 找不到产生式，可能是错误
                        printf("Error: Production not found for reduction: %s -> %s\n", item.prod.left, item.prod.right);
                        continue;
                    }
                    if (action_table[i][(int)item.lookahead].action != 'e' && 
                        (action_table[i][(int)item.lookahead].action != 'r' || action_table[i][(int)item.lookahead].value != prod_num)) {
                        printf("Conflict detected at state %d, symbol %c: existing %c%d, new r%d\n",
                                i, item.lookahead, action_table[i][(int)item.lookahead].action, action_table[i][(int)item.lookahead].value, prod_num);
                    }
                    action_table[i][(int)item.lookahead].action = 'r';
                    action_table[i][(int)item.lookahead].value = prod_num; // 归约动作，值为产生式编号
                }
            }
        }
    }
}

// 打印LR(1)分析表
void print_parsing_table() {
    printf("\nLR(1) Analysis Table: \n");
    printf("state\t");

    for (int i = 0; i < terminal_count; i++) {
        printf("%c\t", terminals[i]);
    }
    printf("|\t");
    for (int i = 0; i < nonterminal_count; i++) {
        if (strcmp(nonterminals + i, "S'") != 0) { // 过滤S'，S'是扩展文法的开始符号
            printf("%c\t", nonterminals[i]); // 打印非终结符
        }
    }
    printf("\n");

    for (int i = 0; i < state_count; i++) {
        printf("%d\t", i);
        for (int j = 0; j < terminal_count; j++) {
            char symbol = terminals[j];
            TableEntry entry = action_table[i][(int)symbol];
            if (entry.action == 's') {
                printf("s%d\t", entry.value);
            } else if (entry.action == 'r') {
                printf("r%d\t", entry.value);
            } else if (entry.action == 'a') {
                printf("acc\t");
            } else {
                printf("\t");
            }
        }
        printf("|\t");
        for (int j = 0; j < nonterminal_count; j++) {
            if (strcmp(nonterminals + j, "S'") != 0) {
                char symbol = nonterminals[j];
                TableEntry entry = goto_table[i][(int)symbol];
                if (entry.action == 'g') {
                    printf("%d\t", entry.value);
                } else {
                    printf("\t");
                }
            }
        }
        printf("\n");
    }
}

// LR(1)语法分析过程
void parse_input(const char* input) {
    int stack_state[MAX_STATES];   // 状态栈
    char stack_symbol[MAX_STATES]; // 符号栈
    int stack_top = 0;

    stack_state[stack_top] = 0; // 初始状态
    stack_symbol[stack_top] = '#'; // 初始符号
    stack_top++;

    char input_buffer[MAX_PROD_LEN + 1];
    strcpy(input_buffer, input);
    strcat(input_buffer, "#"); // 添加结束符

    int input_pos = 0;
    printf("\nLR(1) Parsing Process:\n");
    printf("Step\tState Stack\tSymbol Stack\tInput\t\tAction\n");

    int step = 1;
    while (true) {
        char current_input_symbol = input_buffer[input_pos];
        int current_state = stack_state[stack_top - 1];
        TableEntry entry = action_table[current_state][(int)current_input_symbol];

        // 打印当前状态
        printf("%d\t", step++);
        for (int i = 0; i < stack_top; i++) {
            printf("%d ", stack_state[i]);
        }
        printf("\t\t");
        for (int i = 0; i < stack_top; i++) {
            printf("%c ", stack_symbol[i]);
        }
        printf("\t\t");
        for (int i = input_pos; input_buffer[i] != '\0'; i++) {
            printf("%c", input_buffer[i]);
        }
        printf("\t\t");

        if (entry.action == 's') {
            // 移进
            printf("shift %d\n", entry.value);
            stack_state[stack_top] = entry.value;
            stack_symbol[stack_top] = current_input_symbol;
            stack_top++;
            input_pos++;
        } else if (entry.action == 'r') {
            // 归约
            int prod_num = entry.value;
            int rhs_len = strlen(grammar[prod_num].right);
            char reduce_left = grammar[prod_num].left[0];

            printf("reduce %s -> %s\n", grammar[prod_num].left, grammar[prod_num].right);

            stack_top -= rhs_len;
            if (stack_top < 0) { // 栈为空，但仍需弹出，说明错误
                printf("Error: Stack underflow during reduction.\n");
                break;
            }

            current_state = stack_state[stack_top - 1]; // 归约后的新栈顶状态
            int next_state = goto_table[current_state][(int)reduce_left].value;

            if (goto_table[current_state][(int)reduce_left].action == 'g' && next_state != -1) {
                stack_state[stack_top] = next_state;
                stack_symbol[stack_top] = reduce_left;
                stack_top++;
            } else {
                printf("Error: GOTO[%d, %c] is not defined.\n", current_state, reduce_left);
                break;
            }
        } else if (entry.action == 'a') {
            // 接受
            printf("accept\n");
            break;
        } else { // 'e' or other error
            printf("Error: No action defined for state %d, symbol %c.\n", current_state, current_input_symbol);
            break;
        }
    }
}
