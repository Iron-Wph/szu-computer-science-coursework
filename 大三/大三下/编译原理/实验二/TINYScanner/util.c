/****************************************************/
/* 文件: util.c                                     */
/* TINY 编译器的实用函数实现                         */
/* 编译原理与实践                                   */
/* 肯尼斯·C·劳登                                   */
/****************************************************/

#include "globals.h"
#include "util.h"

// 判断字符串是否包含除了字母和数字以外的其他字符
int hasOtherCharacters(const char *str) {
    int len = strlen(str);
    for (int i = 0; i < len; i++) {
        // 使用 isalnum 函数判断字符是否为字母或数字
        if (!isalnum((unsigned char)str[i])) { 
            // 如果不是字母或数字，则返回 1
            return 1;  
        }
    }
    // 如果所有字符都是字母或数字，则返回 0
    return 0;  
}

// 判断字符串是否全部为数字
int isAllDigits(const char *str) {
    int len = strlen(str);
    for (int i = 0; i < len; i++) {
        if (!isdigit((unsigned char)str[i])) {
            return 0; // 若遇到非数字字符，返回 0
        }
    }
    return 1; // 所有字符都是数字，返回 1
}


/* 过程 printToken 将一个词法单元及其词素打印到列表文件中 */
void printToken(TokenType token, const char* tokenString)
{
    switch (token)
    {
    case IF:
    case THEN:
    case ELSE:
    case END:
    case REPEAT:
    case UNTIL:
    case READ:
    case WRITE:
    // 新增的KEY
    case TRUE1:
    case FALSE1:	
    case OR:
    case AND:
    case NOT:
    case INT:
    case BOOL:
    case STRING:
    case DO:
    case WHILE:
        fprintf(listing,
            "KEY: %s\n", tokenString);
        break;
    case ASSIGN:
        fprintf(listing, 
            "SYM, 值 = %s", ":=\n");
        break;
    case LT:
        fprintf(listing, 
            "SYM, 值 = %s", "<\n");
        break;
    case EQ:
        fprintf(listing,
            "SYM, 值 = %s", "=\n");
        break;
    case LPAREN:
        fprintf(listing, 
            "SYM, 值 = %s", "(\n");
        break;
    case RPAREN:
        fprintf(listing, 
            "SYM, 值 = %s", ")\n");
        break;
    case SEMI:
        fprintf(listing, 
            "SYM, 值 = %s", ";\n");
        break;
    // 新增的符号
    case GT:
        fprintf(listing, 
            "SYM, 值 = %s", ">\n");
        break;
    case LE:
        fprintf(listing, 
            "SYM, 值 = %s", "<=\n");
        break;
    case GE:
        fprintf(listing, 
            "SYM, 值 = %s", ">=\n");
        break;
    case COMMA:
        fprintf(listing, 
            "SYM, 值 = %s", ",\n");
        break;
    case SINGLE_QUOTE:
        fprintf(listing, 
            "SYM, 值 = %s", "'\n");
        break;
    // 
    case PLUS:
        fprintf(listing, 
            "SYM, 值 = %s", "+\n");
        break;
    case MINUS:
        fprintf(listing, 
            "SYM, 值 = %s", "-\n");
        break;
    case TIMES:
        fprintf(listing, 
            "SYM, 值 = %s", "*\n");
        break;
    case OVER:
        fprintf(listing, 
            "SYM, 值 = %s", "/\n");
        break;
    case ENDFILE:
        fprintf(listing, "EOF\n");
        break;
    case NUM:
        // 全都是数字
        if(isAllDigits(tokenString)){
            fprintf(listing,
                "NUM, 值 = %s\n", tokenString);
        }
        else
        {
            fprintf(listing,
                "ERROR: %s the NUM only contains numbers!\n", tokenString);   
        }
        break;
    case ID:
        // 判断标识符是否包含除了字母和数字以外的其他字符
        if (hasOtherCharacters(tokenString)) {
            fprintf(listing,
                "ERROR: %s the ID only contains letters and numbers!\n", tokenString);       
        }
        else
            fprintf(listing,
                "ID, 名称 = %s\n", tokenString);
        break;
    // 处理字符串
    case STR:
        fprintf(listing,
            "STR, 名称 = %s\n", tokenString);
        break;
    case ERROR:
        fprintf(listing,
            "ERROR: %s\n", tokenString);
        break;
    default: /* 永远不应该发生 */
        fprintf(listing, "未知词法单元: %d\n", token);
    }
}

/* 函数 newStmtNode 为语法树构造创建一个新的语句节点 */
TreeNode *newStmtNode(StmtKind kind)
{
    TreeNode *t = (TreeNode *)malloc(sizeof(TreeNode));
    int i;
    if (t == NULL)
        fprintf(listing, "在第 %d 行出现内存不足错误\n", lineno);
    else {
        for (i = 0; i < MAXCHILDREN; i++)
            t->child[i] = NULL;
        t->sibling = NULL;
        t->nodekind = StmtK;
        t->kind.stmt = kind;
        t->lineno = lineno;
    }
    return t;
}

/* 函数 newExpNode 为语法树构造创建一个新的表达式节点 */
TreeNode *newExpNode(ExpKind kind)
{
    TreeNode *t = (TreeNode *)malloc(sizeof(TreeNode));
    int i;
    if (t == NULL)
        fprintf(listing, "在第 %d 行出现内存不足错误\n", lineno);
    else {
        for (i = 0; i < MAXCHILDREN; i++)
            t->child[i] = NULL;
        t->sibling = NULL;
        t->nodekind = ExpK;
        t->kind.exp = kind;
        t->lineno = lineno;
        t->type = Void;
    }
    return t;
}

/* 函数 copyString 分配内存并对现有字符串进行新的复制 */
char *copyString(char *s)
{
    int n;
    char *t;
    if (s == NULL)
        return NULL;
    n = strlen(s) + 1;
    t = malloc(n);
    if (t == NULL)
        fprintf(listing, "在第 %d 行出现内存不足错误\n", lineno);
    else
        strcpy(t, s);
    return t;
}

/* 变量 indentno 被 printTree 用于存储当前需要缩进的空格数 */
static indentno = 0;

/* 用于增加/减少缩进的宏 */
#define INDENT indentno += 2
#define UNINDENT indentno -= 2

/* printSpaces 通过打印空格来实现缩进 */
static void printSpaces(void)
{
    int i;
    for (i = 0; i < indentno; i++)
        fprintf(listing, " ");
}

/* 过程 printTree 将语法树打印到列表文件中，使用缩进表示子树 */
void printTree(TreeNode *tree)
{
    int i;
    INDENT;
    while (tree != NULL) {
        printSpaces();
        if (tree->nodekind == StmtK)
        {
            switch (tree->kind.stmt) {
            case IfK:
                fprintf(listing, "If\n");
                break;
            case RepeatK:
                fprintf(listing, "Repeat\n");
                break;
            case AssignK:
                fprintf(listing, "赋值给: %s\n", tree->attr.name);
                break;
            case ReadK:
                fprintf(listing, "读取: %s\n", tree->attr.name);
                break;
            case WriteK:
                fprintf(listing, "Write\n");
                break;
            default:
                fprintf(listing, "未知的语句节点类型\n");
                break;
            }
        }
        else if (tree->nodekind == ExpK)
        {
            switch (tree->kind.exp) {
            case OpK:
                fprintf(listing, "操作符: ");
                printToken(tree->attr.op, "\0");
                break;
            case ConstK:
                fprintf(listing, "常量: %d\n", tree->attr.val);
                break;
            case IdK:
                fprintf(listing, "标识符: %s\n", tree->attr.name);
                break;
            default:
                fprintf(listing, "未知的表达式节点类型\n");
                break;
            }
        }
        else
            fprintf(listing, "未知的节点类型\n");
        for (i = 0; i < MAXCHILDREN; i++)
            printTree(tree->child[i]);
        tree = tree->sibling;
    }
    UNINDENT;
}