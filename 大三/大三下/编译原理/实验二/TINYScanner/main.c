/****************************************************/
/* 文件: main.c                                     */
/* TINY 编译器的主程序                             */
/* 编译原理与实践                                   */
/* 肯尼斯·C·劳登                                   */
/****************************************************/

#include "globals.h"

/* 将 NO_PARSE 设置为 TRUE 可得到仅含词法分析器的编译器 */
#define NO_PARSE TRUE
/* 将 NO_ANALYZE 设置为 TRUE 可得到仅含语法分析器的编译器 */
#define NO_ANALYZE TRUE

/* 将 NO_CODE 设置为 TRUE 可得到不生成代码的编译器 */
#define NO_CODE FALSE

#include "util.h"
#include "scan.h"

/* 分配全局变量 */
int lineno = 0;
FILE * source;
FILE * listing;
FILE * code;

/* 分配并设置跟踪标志 */
int EchoSource = TRUE;
int TraceScan = TRUE;
int TraceParse = TRUE;
int TraceAnalyze = FALSE;
int TraceCode = FALSE;

int Error = FALSE;

// 主函数
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
    fprintf(listing,"\nTINY 编译: %s\n\n",pgm);

    while (getToken()!=ENDFILE);

    fclose(source);
    // 此为 Windows 下暂停命令，在 Linux 等系统中无意义，可根据实际情况修改
    // system("pause"); 
    printf("Press Enter to continue...");
    getchar();
    return 0;
}