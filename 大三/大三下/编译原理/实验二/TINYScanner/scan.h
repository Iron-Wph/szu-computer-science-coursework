/****************************************************/
/* 文件: scan.h                                     */
/* TINY 编译器的词法分析器接口                       */
/* 编译原理与实践                                   */
/* 肯尼斯·C·劳登                                   */
/****************************************************/

#ifndef _SCAN_H_
#define _SCAN_H_

/* MAXTOKENLEN 是一个词法单元的最大长度 */
#define MAXTOKENLEN 40

/* tokenString 数组用于存储每个词法单元的词素 */
extern char tokenString[MAXTOKENLEN + 1];

/* 函数 getToken 返回源文件中的下一个词法单元 */
TokenType getToken(void);

#endif