/****************************************************/
/* 文件: scan.c                                     */
/* TINY 编译器的扫描器实现                           */
/* 《编译器构造：原理与实践》                        */
/* 作者: Kenneth C. Louden                            */
/****************************************************/

#include "globals.h"
#include "util.h"
#include "scan.h"

/* 扫描器有限自动机（DFA）中的状态 */
typedef enum
   { START,INASSIGN,INCOMMENT,INNUM,INID,INGREAT,INLESS,INSTR,DONE }
   StateType;

/* 标识符或保留字的词素 */
char tokenString[MAXTOKENLEN + 1];

/* BUFLEN = 用于存储源代码行的输入缓冲区长度 */
#define BUFLEN 256

static char lineBuf[BUFLEN]; /* 保存当前行 */
static int linepos = 0; /* lineBuf 中的当前位置 */
static int bufsize = 0; /* 缓冲区字符串的当前大小 */
static int EOF_flag = FALSE; /* 修正 EOF 时 ungetNextChar 函数的行为 */

/* getNextChar 从 lineBuf 中获取下一个非空白字符，
   如果 lineBuf 已耗尽，则读取新的一行 */
static int getNextChar(void)
{ 
    if (!(linepos < bufsize))
    { 
        lineno++;
        if (fgets(lineBuf, BUFLEN - 1, source))
        { 
            if (EchoSource) fprintf(listing, "%4d: %s", lineno, lineBuf);
            bufsize = strlen(lineBuf);
            linepos = 0;
            return lineBuf[linepos++];
        }
        else
        { 
            EOF_flag = TRUE;
            return EOF;
        }
    }
    else return lineBuf[linepos++];
}

/* ungetNextChar 在 lineBuf 中回退一个字符 */
static void ungetNextChar(void)
{ 
    if (!EOF_flag) linepos-- ;
}

/* 保留字查找表 */
static struct
    { 
        char* str;
        TokenType tok;
    } reservedWords[MAXRESERVED]
   = {{"if",IF},{"then",THEN},{"else",ELSE},{"end",END},
      {"repeat",REPEAT},{"until",UNTIL},{"read",READ},
      {"write",WRITE},
      {"true",T_TRUE},
      {"false",T_FALSE},
      {"not",NOT},
      {"and",AND},
      {"or",OR},
      {"int",INT},
      {"string",STRING},
      {"bool",BOOL},
      {"do",DO},
      {"while",WHILE}
     };

/* 查找一个标识符，看它是否是一个保留字 */
/* 使用线性搜索 */
static TokenType reservedLookup (char * s)
{ 
    int i;
    for (i = 0; i < MAXRESERVED; i++)
        if (!strcmp(s, reservedWords[i].str))
            return reservedWords[i].tok;
    return ID;
}


/* 错误代码部分 **/

int errorCode = 0;		
char *errorMsg[6] = {
    "未知错误",
    "注释不完整，缺少 }!",
    "注释错误，意外的 {!",
    "字符串不完整，缺少 '!",
    "字符串不能包含换行符",
    "非法字符"
};
#define ERR_UNKOWN 0
#define ERR_COMMENT_US 1
#define ERR_COMMENT_CE 2
#define ERR_STRING_US 3
#define ERR_STRING_RETURN 4
#define ERR_CHAR_IL 5

/*                 */


/****************************************/
/* 扫描器的主要函数                      */
/****************************************/
/* 函数 getToken 返回源文件中的下一个标记 */
TokenType getToken(void)
{  
    /* 用于存储到 tokenString 的索引 */
    int tokenStringIndex = 0;
    /* 保存当前要返回的标记 */
    TokenType currentToken;
    /* 当前状态 - 总是从 START 开始 */
    StateType state = START;
    /* 用于指示是否保存到 tokenString 的标志 */
    int save;
    while (state != DONE)
    { 
        int c = getNextChar();
        save = TRUE;
        switch (state)
        { 
            case START:
                if (isdigit(c))
                    state = INNUM;
                else if (isalpha(c))
                    state = INID;
                else if (c == '<') 
                    state = INLESS;
                else if (c == '>') 
                    state = INGREAT;
                else if (c == '\'') {
                    state = INSTR;
                }
                else if (c == ':')
                    state = INASSIGN;
                else if ((c == ' ') || (c == '\t') || (c == '\n')|| (c == '\r'))
                    save = FALSE;
                else if (c == '{')
                { 
                    save = FALSE;
                    state = INCOMMENT;
                }
                else 
                { 
                    state = DONE;
                    switch (c)
                    { 
                        case EOF:
                            save = FALSE;
                            currentToken = ENDFILE;
                            break;
                        case '=':
                            currentToken = EQ;
                            break;
                        case '+':
                            currentToken = PLUS;
                            break;
                        case '-':
                            currentToken = MINUS;
                            break;
                        case '*':
                            currentToken = TIMES;
                            break;
                        case '/':
                            currentToken = OVER;
                            break;
                        case '(':
                            currentToken = LPAREN;
                            break;
                        case ')':
                            currentToken = RPAREN;
                            break;
                        case ';':
                            currentToken = SEMI;
                            break;
                        case ',':
                            currentToken = COMMA;
                            break;
                        default:
                            if (!isLegalChar(c)) {
                                currentToken = ERROR;
                                errorCode = ERR_CHAR_IL;
                                break;
                            }
                            currentToken = ERROR;
                            errorCode = ERR_UNKOWN;
                            break;
                    }
                }
                break;
            case INCOMMENT:
                save = FALSE;
                if (c == EOF)
                { 
                    state = DONE;
                    currentToken = ERROR;
                    errorCode = ERR_COMMENT_US;
                }
                else if (c == '}') state = START;
                else if (c == '{') {
                    state = DONE;
                    currentToken = ERROR;
                    errorCode = ERR_COMMENT_CE;
                }
                break;
            case INASSIGN:
                state = DONE;
                if (c == '=')
                    currentToken = ASSIGN;
                else
                { 
                    /* 回退输入 */
                    ungetNextChar();
                    save = FALSE;
                    currentToken = ERROR;
                }
                break;
            case INNUM:
                if (!isdigit(c))
                { 
                    /* 回退输入 */
                    ungetNextChar();
                    save = FALSE;
                    state = DONE;
                    currentToken = NUM;
                }
                break;
            case INID:
                if (!isalpha(c)&&!isdigit(c))
                { 
                    /* 回退输入 */
                    ungetNextChar();
                    save = FALSE;
                    state = DONE;
                    currentToken = ID;
                }
                break;
            case INLESS:
                state = DONE;
                if (c == '=')
                    currentToken = LTE;
                else
                { 
                    ungetNextChar();
                    currentToken = LT;
                    save = FALSE;
                }
                break;
            case INGREAT:
                state = DONE;
                if (c == '=')
                    currentToken = GTE;
                else
                { 
                    ungetNextChar();
                    currentToken = GT;
                    save = FALSE;
                }
                break;
            case INSTR:
                if (c == '\'') {
                    currentToken = STR;
                    state = DONE;
                }
                else if (c == '\n' )  // 换行符
                { 
                    ungetNextChar();
                    currentToken = ERROR ;
                    errorCode = ERR_STRING_RETURN;
                    save = FALSE;
                    state = DONE;
                }
                else if (c == EOF) {
                    currentToken = ERROR;
                    errorCode = ERR_STRING_US;
                    save = FALSE;
                    state = DONE;
                }
                break;
            case DONE:
            default: /* 不应该发生 */
                fprintf(listing, "扫描器错误: 状态 = %d\n", state);
                state = DONE;
                currentToken = ERROR;
                break;
        }
        if ((save) && (tokenStringIndex <= MAXTOKENLEN))
            tokenString[tokenStringIndex++] = (char) c;
        if (state == DONE)
        { 
            tokenString[tokenStringIndex] = '\0';
            if (currentToken == ID)
                currentToken = reservedLookup(tokenString);
        }
    }
    if (TraceScan) {
        fprintf(listing, "\t%d: ", lineno);
        printToken(currentToken, tokenString);
    }
    return currentToken;
} /* end getToken */