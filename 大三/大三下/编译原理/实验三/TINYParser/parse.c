/****************************************************/
/* 文件: parse.c                                    */
/* TINY 编译器的解析器实现                           */
/* 《编译器构造：原理与实践》                        */
/* 作者: Kenneth C. Louden                            */
/****************************************************/

#include "globals.h"
#include "util.h"
#include "scan.h"
#include "parse.h"

// 保存当前的标记
static TokenType token; 

// 递归调用的函数原型
static TreeNode * stmt_sequence(void);
static TreeNode * statement(void);
static TreeNode * if_stmt(void);
static TreeNode * repeat_stmt(void);
static TreeNode * assign_stmt(void);
static TreeNode * read_stmt(void);
static TreeNode * write_stmt(void);
static TreeNode * _exp(void);
static TreeNode * simple_exp(void);
static TreeNode * term(void);
static TreeNode * factor(void);
// 新增产生式
static TreeNode * declarations(void);
static TreeNode * decl(void);
static TreeNode * type_specifier(void);
static TreeNode * varlist(void);
static TreeNode * while_stmt(void);


// 输出语法错误信息
static void syntaxError(char * message)
{ 
    // 输出错误提示信息
    fprintf(listing,"\n>>> ");
    // 输出错误发生的行号和具体错误信息
    fprintf(listing,"第 %d 行发生语法错误: %s",lineno,message);
    // 标记发生错误
    Error = TRUE;
}

// 匹配期望的标记
static void match(TokenType expected)
{ 
    // 如果当前标记与期望标记相同，获取下一个标记
    if (token == expected) token = getToken();
    else {
        // 输出语法错误信息
        syntaxError("意外的标记 -> ");
        // 打印当前标记
        printToken(token,tokenString);
        fprintf(listing,"      ");
    }
}

// 解析语句序列
TreeNode * stmt_sequence(void)
{ 
    // 解析一条语句
    TreeNode * t = statement();
    TreeNode * p = t;
    // 当未到文件结尾，未遇到 END、ELSE、UNTIL 标记时继续解析
    // 新增while语句
    while ((token!=ENDFILE) && (token!=END) &&
           (token!=ELSE) && (token!=UNTIL) && (token!=WHILE))
    { 
        TreeNode * q;
        // 匹配分号
        match(SEMI);
        // 解析下一条语句
        q = statement();
        if (q!=NULL) {
            if (t==NULL) t = p = q;
            else {
                // 将新语句作为兄弟节点连接
                p->sibling = q;
                p = q;
            }
        }
    }
    return t;
}

// 解析单条语句
TreeNode * statement(void)
{ 
    TreeNode * t = NULL;
    switch (token) {
        // 解析 if 语句
        case IF : t = if_stmt(); break;
        // 解析 repeat 语句
        case REPEAT : t = repeat_stmt(); break;
        // 解析赋值语句
        case ID : t = assign_stmt(); break;
        // 解析 read 语句
        case READ : t = read_stmt(); break;
        // 解析 write 语句
        case WRITE : t = write_stmt(); break;
        // 新增解析while语句，以"DO"开头
        case DO : t = while_stmt(); break;
        default : 
            // 输出语法错误信息
            syntaxError("意外的标记 -> ");
            // 打印当前标记
            printToken(token,tokenString);
            // 获取下一个标记
            token = getToken();
            break;
    } 
    return t;
}

// 解析 if 语句
TreeNode * if_stmt(void)
{ 
    // 创建一个 if 语句节点
    TreeNode * t = newStmtNode(IfK);
    // 匹配 IF 标记
    match(IF);
    if (t!=NULL) t->child[0] = _exp();
    // 匹配 THEN 标记
    match(THEN);
    if (t!=NULL) t->child[1] = stmt_sequence();
    if (token==ELSE) {
        // 匹配 ELSE 标记
        match(ELSE);
        if (t!=NULL) t->child[2] = stmt_sequence();
    }
    // 匹配 END 标记
    match(END);
    return t;
}

// 解析 repeat 语句
TreeNode * repeat_stmt(void)
{ 
    // 创建一个 repeat 语句节点
    TreeNode * t = newStmtNode(RepeatK);
    // 匹配 REPEAT 标记
    match(REPEAT);
    if (t!=NULL) t->child[0] = stmt_sequence();
    // 匹配 UNTIL 标记
    match(UNTIL);
    if (t!=NULL) t->child[1] = _exp();
    return t;
}

// 解析赋值语句
TreeNode * assign_stmt(void)
{ 
    // 创建一个赋值语句节点
    TreeNode * t = newStmtNode(AssignK);
    if ((t!=NULL) && (token==ID))
        t->attr.name = copyString(tokenString);
    // 匹配 ID 标记
    match(ID);
    // 匹配赋值符号
    match(ASSIGN);
    if (t!=NULL) t->child[0] = _exp();
    return t;
}

// 解析 read 语句
TreeNode * read_stmt(void)
{ 
    // 创建一个 read 语句节点
    TreeNode * t = newStmtNode(ReadK);
    // 匹配 READ 标记
    match(READ);
    if ((t!=NULL) && (token==ID))
        t->attr.name = copyString(tokenString);
    // 匹配 ID 标记
    match(ID);
    return t;
}

// 解析 write 语句
TreeNode * write_stmt(void)
{ 
    // 创建一个 write 语句节点
    TreeNode * t = newStmtNode(WriteK);
    // 匹配 WRITE 标记
    match(WRITE);
    if (t!=NULL) t->child[0] = _exp();
    return t;
}

// 解析表达式
TreeNode * _exp(void)
{ 
    // 解析简单表达式
    TreeNode * t = simple_exp();
    // 新增bool: 补充大于、大于等于和小于等于的节点创建
    if ((token==LT)||(token==EQ) || (token==LTE) || (token==GTE) || (token==GT)) {
        // 创建一个操作符节点
        TreeNode * p = newExpNode(OpK);
        if (p!=NULL) {
            p->child[0] = t;
            p->attr.op = token;
            t = p;
        }
        // 匹配操作符
        match(token);
        if (t!=NULL)
            t->child[1] = simple_exp();
    }
    return t;
}

// 解析简单表达式
TreeNode * simple_exp(void)
{ 
    // 解析项
    TreeNode * t = term();
    while ((token==PLUS)||(token==MINUS))
    { 
        // 创建一个操作符节点
        TreeNode * p = newExpNode(OpK);
        if (p!=NULL) {
            p->child[0] = t;
            p->attr.op = token;
            t = p;
            // 匹配操作符
            match(token);
            t->child[1] = term();
        }
    }
    return t;
}

// 解析项
TreeNode * term(void)
{ 
    // 解析因子
    TreeNode * t = factor();
    while ((token==TIMES)||(token==OVER))
    { 
        // 创建一个操作符节点
        TreeNode * p = newExpNode(OpK);
        if (p!=NULL) {
            p->child[0] = t;
            p->attr.op = token;
            t = p;
            // 匹配操作符
            match(token);
            p->child[1] = factor();
        }
    }
    return t;
}

// 解析因子
TreeNode * factor(void)
{ 
    TreeNode * t = NULL;
    switch (token) {
        case NUM :
            // 创建一个常量节点
            t = newExpNode(ConstK);
            if ((t!=NULL) && (token==NUM))
                t->attr.val = atoi(tokenString);
            // 匹配数字标记
            match(NUM);
            break;
        case ID :
            // 创建一个标识符节点
            t = newExpNode(IdK);
            if ((t!=NULL) && (token==ID))
                t->attr.name = copyString(tokenString);
            // 匹配标识符标记
            match(ID);
            break;
        case LPAREN :
            // 匹配左括号
            match(LPAREN);
            t = _exp();
            // 匹配右括号
            match(RPAREN);
            break;
        // 新增字符串
        case STR :
            // 创建一个字符串节点
            t = newExpNode(StrK);
            if ((t!=NULL) && (token==STR))
                t->attr.name = copyString(tokenString);
            // 匹配字符串标记
            match(STR);
            break;
        default:
            // 输出语法错误信息
            syntaxError("意外的标记 -> ");
            // 打印当前标记
            printToken(token,tokenString);
            // 获取下一个标记
            token = getToken();
            break;
    }
    return t;
}

/****************************************/
/* 解析器的主要函数                      */
/****************************************/
/* 解析函数返回新构建的语法树             */
TreeNode * parse(void)
{ 
    TreeNode * t = newStmtNode(ProgramK); // 创建一个程序节点
    // 获取第一个标记
    token = getToken();
    // 新增一个孩子节点，用于delclarations
    if (token == INT || token == BOOL || token == STRING)
    {
        t->child[0] = declarations();
        t->child[1] = stmt_sequence();
    }
    else{
        t->child[0] = stmt_sequence();
    }
    
    if (token!=ENDFILE)
        // 输出语法错误信息
        syntaxError("代码在文件结束前结束\n");
    return t;
}

static TreeNode * declarations(void)
{
    TreeNode * t = NULL;
    TreeNode * p = NULL;
    // 如果token是类型标记，继续解析
    while ((token == INT) || (token == BOOL) || (token == STRING))
    {
        // 匹配值类型
        TreeNode * q = decl();
        // 匹配分号
        match(SEMI);
        if (t == NULL)
        {
            t = q;  p = q;
        }
        else
        {   
            // 将新声明作为兄弟节点连接
            p->sibling = q;  p = q;
        }
    }
    return t;
}


static TreeNode * decl(void)
{
    TreeNode * t = type_specifier();
    t->child[0] = varlist();
    return t;
}

static TreeNode * type_specifier(void)
{
    TreeNode * t = NULL;
    switch (token) {
        case INT:
            // 新增创建一个类型节点
            t = newTypeNode(IntK);
            // 匹配数字标记
            match(INT);
            break;
        case BOOL:
            // 新增创建一个类型节点
            t = newTypeNode(BoolK);
            // 匹配数字标记
            match(BOOL);
            break;
        case STRING:
            // 新增创建一个类型节点
            t = newTypeNode(StringK);
            // 匹配数字标记
            match(STRING);
            break;
        default:
            // 输出语法错误信息
            syntaxError("意外的标记 -> ");
            // 打印当前标记
            printToken(token,tokenString);
            // 获取下一个标记
            token = getToken();
            break;
    }
    return t;
}


static TreeNode * varlist(void)
{
    TreeNode * t = NULL;
    TreeNode * p = NULL;
    // 当 token 为 ID 时进入循环
    while (token == ID)
    {
        // 创建一个类型为 IdK 的表达式节点，并将其地址赋给 q
        TreeNode * q = newExpNode(IdK);
        q->attr.name = copyString(tokenString);
        // 匹配 ID 类型的 token
        match(ID);
        // 如果 t 为 NULL
        if (t == NULL)
        {
            t = q;  p = q;
        }
        else
        {   // 因为多个id为父子关系
            p->child[0] = q;  p = q;
        }

        // 如果 token 为 COMMA，则匹配；反之，退出循环
        if (token == COMMA)
            match(COMMA);
        else
            break;
    }
    return t;
}

static TreeNode * while_stmt(void)
{
    // 创建一个 while 语句节点
    TreeNode * t = newStmtNode(WhileK);
    // 匹配 do 标记
    match(DO);
    if (t!=NULL) t->child[0] = stmt_sequence();
    // 匹配 while 标记
    match(WHILE);
    // bool exp通过_exp()函数解析
    if (t!=NULL) t->child[1] = _exp();
    return t;
}