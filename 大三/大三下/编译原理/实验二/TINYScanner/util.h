/****************************************************/
/* 文件：util.h                                     */
/* TINY 编译器的实用函数                              */
/* 编译原理与实践                                   */
/* 肯尼斯·C·劳登                                   */
/****************************************************/

#ifndef _UTIL_H_
#define _UTIL_H_

/* 过程 printToken 将一个词法单元及其词素打印到列表文件中 */
void printToken( TokenType, const char* );

/* 函数 newStmtNode 为语法树构造创建一个新的语句节点 */
TreeNode * newStmtNode(StmtKind);

/* 函数 newExpNode 为语法树构造创建一个新的表达式节点 */
TreeNode * newExpNode(ExpKind);

/* 函数 copyString 分配内存并对现有字符串进行新的复制 */
char * copyString( char * );

/* 过程 printTree 将语法树打印到列表文件中，使用缩进表示子树 */
void printTree( TreeNode * );

#endif