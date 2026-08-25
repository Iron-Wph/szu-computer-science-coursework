/****************************************************/
/* 文件: main.c                                     */
/* TINY 编译器的主程序                              */
/* 《编译器构造：原理与实践》                        */
/* 作者: Kenneth C. Louden                            */
/****************************************************/

#include "globals.h"

/* 将 NO_PARSE 设置为 TRUE 可得到仅含扫描器的编译器 */
#define NO_PARSE FALSE

#include "util.h"
#if NO_PARSE
#include "scan.h"
#else
#include "parse.h"
#endif

/* 分配全局变量 */
int lineno = 0;
FILE * source;
FILE * listing;
FILE * code;

/* 分配并设置跟踪标志 */
int EchoSource = TRUE;
int TraceScan = TRUE;
int TraceParse = TRUE;

int Error = FALSE;

int main( int argc, char * argv[] )
{
    TreeNode * syntaxTree;
    char pgm[120]; /* 源代码文件名 */
    if (argc != 2)
    {
        fprintf(stderr,"用法: %s <文件名>\n",argv[0]);
        exit(1);
    }
    strcpy(pgm,argv[1]) ;
    if (strchr (pgm, '.') == NULL)
        strcat(pgm,".tny");
    source = fopen(pgm,"r");
    if (source==NULL)
    {
        fprintf(stderr,"文件 %s 未找到\n",pgm);
        exit(1);
    }
    listing = stdout; /* 将列表输出到屏幕 */
    fprintf(listing,"\nTINY 编译: %s\n",pgm);
#if NO_PARSE
    while (getToken()!=ENDFILE);
#else
    syntaxTree = parse();
    if (TraceParse) {
        fprintf(listing,"\n语法树:\n");
        printTree(syntaxTree);
    }
#endif
    fclose(source);
    system("pause");
    return 0;
}