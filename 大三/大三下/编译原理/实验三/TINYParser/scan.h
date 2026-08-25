/****************************************************/
/* 文件: scan.h                                     */
/* TINY 编译器的扫描器接口                           */
/* 《编译器构造：原理与实践》                        */
/* 作者: Kenneth C. Louden                            */
/****************************************************/

#ifndef _SCAN_H_
#define _SCAN_H_

/* MAXTOKENLEN 是一个标记的最大长度 */
#define MAXTOKENLEN 40

/* tokenString 数组存储每个标记的词素 */
extern char tokenString[MAXTOKENLEN + 1];

/* 函数 getToken 返回源文件中的下一个标记 */
TokenType getToken(void);

#endif