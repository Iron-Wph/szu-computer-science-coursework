/****************************************************/
/* 文件: util.h                                     */
/* TINY 编译器的实用函数                              */
/* 《编译器构造：原理与实践》                        */
/* 作者: Kenneth C. Louden                            */
/****************************************************/

#ifndef _UTIL_H_
#define _UTIL_H_

/* 过程 printToken 向列表文件打印一个标记及其词素 */
void printToken(TokenType, const char*);

/* 函数 newStmtNode 为语法树构造创建一个新的语句节点 */
TreeNode* newStmtNode(StmtKind);

/* 函数 newExpNode 为语法树构造创建一个新的表达式节点 */
TreeNode* newExpNode(ExpKind);

// 新增创建类型的语法节点
TreeNode* newTypeNode(TypeKind);

/* 函数 copyString 分配内存并对现有字符串进行新的复制 */
char* copyString(char*);

/* 过程 printTree 使用缩进表示子树，将语法树打印到列表文件中 */
void printTree(TreeNode*);

#endif