/****************************************************/
/* 文件: globals.h                                  */
/* TINY 编译器的全局类型和变量                      */
/* 必须在其他头文件之前包含                         */
/* 编译原理与实践                                   */
/* 肯尼斯·C·劳登                                   */
/****************************************************/

#ifndef _GLOBALS_H_
#define _GLOBALS_H_

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#ifndef FALSE
#define FALSE 0
#endif

#ifndef TRUE
#define TRUE 1
#endif

/* MAXRESERVED = 保留字的数量 */
#define MAXRESERVED 18

typedef enum 
{
    /* 用于记录的词法单元 */
    ENDFILE, ERROR,
    /* 保留字 */
    IF, THEN, ELSE, END, REPEAT, UNTIL, READ, WRITE,
    // 新增的保留字
    TRUE1, FALSE1, OR, AND, NOT, INT, BOOL, STRING, DO, WHILE,
    /* 多字符词法单元 */
    ID, NUM,
    /* 特殊符号 */
    ASSIGN, EQ, LT, PLUS, MINUS, TIMES, OVER, LPAREN, RPAREN, SEMI,
    // 新增特殊符号 : >	<=	>=	, '  
    GT, LE, GE, COMMA,SINGLE_QUOTE, 
    // 新增字符串
    STR
} TokenType;

extern FILE* source; /* 源代码文本文件 */
extern FILE* listing; /* 列表输出文本文件 */
extern FILE* code; /* TM 模拟器的代码文本文件 */

extern int lineno; /* 用于列表的源文件行号 */

/**************************************************/
/***********   用于语法分析的语法树 ************/
/**************************************************/

typedef enum {StmtK, ExpK} NodeKind;
typedef enum {IfK, RepeatK, AssignK, ReadK, WriteK} StmtKind;
typedef enum {OpK, ConstK, IdK} ExpKind;

/* ExpType 用于类型检查 */
typedef enum {Void, Integer, Boolean} ExpType;

#define MAXCHILDREN 3

typedef struct treeNode
{
    struct treeNode * child[MAXCHILDREN];
    struct treeNode * sibling;
    int lineno;
    NodeKind nodekind;
    union { StmtKind stmt; ExpKind exp;} kind;
    union { TokenType op;
            int val;
            char * name; } attr;
    ExpType type; /* 用于表达式的类型检查 */
} TreeNode;

/**************************************************/
/***********   用于跟踪的标志       ************/
/**************************************************/

/* EchoSource = TRUE 会使在语法分析过程中，源程序连同行号一起被输出到列表文件中 */
extern int EchoSource;

/* TraceScan = TRUE 会使当词法分析器识别出每个词法单元时，将词法单元信息打印到列表文件中 */
extern int TraceScan;

/* TraceParse = TRUE 会使语法树以线性化的形式（使用缩进表示子树）打印到列表文件中 */
extern int TraceParse;

/* TraceAnalyze = TRUE 会使符号表的插入和查找操作被报告到列表文件中 */
extern int TraceAnalyze;

/* TraceCode = TRUE 会使在生成代码时，注释被写入到 TM 代码文件中 */
extern int TraceCode;

/* Error = TRUE 会在发生错误时阻止进一步的处理阶段 */
extern int Error; 
#endif