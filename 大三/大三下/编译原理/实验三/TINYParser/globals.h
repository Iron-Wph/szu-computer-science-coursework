/****************************************************/
/* 文件: globals.h                                  */
/* TINY 编译器的全局类型和变量                      */
/* 必须在其他头文件包含之前引入                      */
/* 《编译器构造：原理与实践》                        */
/* 作者: Kenneth C. Louden                            */
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
    /* 记录用的标记 */
   {ENDFILE,ERROR,
    /* 保留字 */
    IF,THEN,ELSE,END,REPEAT,UNTIL,READ,WRITE,
	T_TRUE,T_FALSE,OR,AND,NOT,INT,BOOL,STRING,DO,WHILE,
    /* 多字符标记 */
    ID,NUM,STR,
    /* 特殊符号 */
    ASSIGN,EQ,LT,GT,LTE,GTE,PLUS,MINUS,TIMES,OVER,LPAREN,RPAREN,SEMI,COMMA,SQM
   } TokenType;

extern FILE* source; /* 源代码文本文件 */
extern FILE* listing; /* 列表输出文本文件 */
extern FILE* code; /* TM 模拟器的代码文本文件 */

extern int lineno; /* 用于列表输出的源代码行号 */

/**************************************************/
/***********   用于解析的语法树 ************/
/**************************************************/

// 新增类型节点
typedef enum {StmtK,ExpK, TypeK} NodeKind;
// 新增语句节点
typedef enum {IfK,RepeatK,AssignK,ReadK,WriteK,WhileK,ProgramK} StmtKind;
typedef enum {OpK,ConstK,IdK,StrK} ExpKind;
// 新增创建类型的语法节点
typedef enum {IntK, BoolK, StringK} TypeKind;

/* ExpType 用于类型检查 */
typedef enum {Void,Integer,Boolean} ExpType;

#define MAXCHILDREN 3

typedef struct treeNode
   { struct treeNode * child[MAXCHILDREN];
     struct treeNode * sibling;
     int lineno;
     NodeKind nodekind;
     // 新增类型
     union { StmtKind stmt; ExpKind exp; TypeKind type;} kind;
     union { TokenType op;
             int val;
             char * name; } attr;
     ExpType type; /* 用于表达式的类型检查 */
   } TreeNode;

/**************************************************/
/***********   跟踪标志 ************/
/**************************************************/

/* EchoSource 为 TRUE 时，在解析过程中会将源代码及行号回显到列表文件中 */
/***  错误 **/
#define MAX_ERROR 6
extern int errorCode;
extern char *errorMsg[MAX_ERROR];

extern int EchoSource;

/* TraceScan 为 TRUE 时，扫描器识别每个标记时会将标记信息打印到列表文件中 */
extern int TraceScan;

/* TraceParse 为 TRUE 时，会将语法树以线性化形式（使用缩进表示子节点）打印到列表文件中 */
extern int TraceParse;

/* TraceAnalyze 为 TRUE 时，符号表的插入和查找操作会报告到列表文件中 */
extern int TraceAnalyze;

/* TraceCode 为 TRUE 时，代码生成时会在 TM 代码文件中写入注释 */
extern int TraceCode;

/* Error 为 TRUE 时，若发生错误则阻止后续处理 */
extern int Error; 
#endif