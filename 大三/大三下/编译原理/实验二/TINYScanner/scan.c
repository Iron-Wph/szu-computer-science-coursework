/****************************************************/
/* 文件: scan.c                                     */
/* TINY 编译器的词法分析器实现                      */
/* 编译原理与实践                                   */
/* 肯尼斯·C·劳登                                   */
/****************************************************/

#include "globals.h"
#include "util.h"
#include "scan.h"

/* 词法分析器有限状态自动机（DFA）的状态 */
typedef enum
{
    START,      // 起始状态
    INASSIGN,   // 正在处理赋值符号状态
    // 正在处理 >= 和 <=状态
    INGE,       
    INLE,       
    // 正在处理字符串
    INSTRING,
    INCOMMENT,  // 正在处理注释状态
    INNUM,      // 正在处理数字状态
    INID,       // 正在处理标识符状态
    DONE        // 完成状态
} StateType;

/* 标识符或保留字的词素 */
char tokenString[MAXTOKENLEN + 1];

/* BUFLEN = 源代码行输入缓冲区的长度 */
#define BUFLEN 256

static char lineBuf[BUFLEN];  // 保存当前行
static int linepos = 0;       // 当前在 lineBuf 中的位置
static int bufsize = 0;       // 当前缓冲区字符串的大小
static int EOF_flag = FALSE;  // 修正 EOF 时 ungetNextChar 的行为

/* getNextChar 从 lineBuf 中获取下一个非空白字符，
   如果 lineBuf 用完则读取新的一行 */
static int getNextChar(void)
{
    if (!(linepos < bufsize))
    {
        lineno++;
        if (fgets(lineBuf, BUFLEN - 1, source))
        {
            if (EchoSource)
                fprintf(listing, "%d: %s", lineno, lineBuf);
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
    else
        return lineBuf[linepos++];
}

/* ungetNextChar 回退 lineBuf 中的一个字符 */
static void ungetNextChar(void)
{
    // 如果文件未结束，则回退一个字符
    if (!EOF_flag)
        linepos--;
}

/* 保留字查找表 */
static struct
{
    char *str;
    TokenType tok;
} reservedWords[MAXRESERVED] = {{"if", IF}, {"then", THEN}, {"else", ELSE}, {"end", END},
                                {"repeat", REPEAT}, {"until", UNTIL}, {"read", READ},{"write", WRITE},
                                // 添加新的关键字
                                {"true", TRUE1}, {"false", FALSE1}, {"or", OR}, {"and", AND},
                                {"not", NOT}, {"int", INT}, {"bool", BOOL}, {"string", STRING},
                                {"do", DO}, {"while", WHILE}
                            };

/* 查找一个标识符是否为保留字，使用线性查找 */
static TokenType reservedLookup(char *s)
{
    int i;
    for (i = 0; i < MAXRESERVED; i++)
        if (!strcmp(s, reservedWords[i].str))
            return reservedWords[i].tok;
    return ID;
}

/****************************************/
/* 词法分析器的主要函数                 */
/****************************************/
/* getToken 函数返回源文件中的下一个词法单元 */
TokenType getToken(void)
{
    /* 用于存储到 tokenString 的索引 */
    int tokenStringIndex = 0;
    /* 保存当前要返回的词法单元 */
    TokenType currentToken;
    /* 当前状态，总是从 START 开始 */
    StateType state = START;
    /* 标志，指示是否保存到 tokenString */
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
            else if (c == ':')
                state = INASSIGN;
            // 处理 >= 和 <=
            else if(c == '>')
                state = INGE;
            else if (c == '<')
                state = INLE;
            // 处理字符串
            else if (c == '\'')
            {
                // 不保存单引号
                save = FALSE;
                state = INSTRING;
            }
            // 处理注释
            else if (c == '{')
            {
                save = FALSE;
                state = INCOMMENT;
            }
            // 文件格式符号不保存
            else if ((c == ' ') || (c == '\t') || (c == '\n') || (c == '\r'))
                save = FALSE;
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
                case '\'':
                    currentToken = SINGLE_QUOTE;
                    break;
                default:
                    currentToken = ERROR;
                    sprintf(tokenString, "Illegal -> meet the unknown symbol: ", c);
                    tokenStringIndex += strlen(tokenString);
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
                strcpy(tokenString, "the comment is not ended !");
                tokenStringIndex += strlen(tokenString);
                // currentToken = ENDFILE;
            }
            else if (c == '{')
            {
                ungetNextChar();
                state = DONE;
                currentToken = ERROR;
                strcpy(tokenString, "the comment can not be included !");
                tokenStringIndex += strlen(tokenString);
            }
            else if (c == '}')
                state = START;
            break;
        case INASSIGN:
            state = DONE;
            if (c == '=')
                currentToken = ASSIGN;
            else
            {
                /* 回退输入 */
                // 因为不是 := 的符号就会报错
                ungetNextChar();
                save = FALSE;
                currentToken = ERROR;
            }
            break;
        // 处理 >= 和 <=
        case INGE:
            state = DONE;
            if (c == '=')
                currentToken = GE;
            else
            {
                ungetNextChar();
                currentToken = GT;
            }
            break;
        case INLE:
            state = DONE;
            if (c == '=')
                currentToken = LE;
            else
            {
                ungetNextChar();
                currentToken = LT;
            }
            break;
        // 处理字符串
        case INSTRING:
            if (c == '\'')
            {
                save = FALSE;
                state = DONE;
                currentToken = STR;
            }
            // 不能超过一行，即字符串不能跨行
            else if (linepos >= bufsize)
            {
                save = FALSE;
                state = DONE;
                currentToken = ERROR;
                strcpy(tokenString, "the string must be a line or misses the \' ！");
                tokenStringIndex += strlen(tokenString);
            }
            break;
        case INNUM:
            // 空白字符分割标识符 或 遇到运算符号
            if (c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == EOF 
                || c == ',' || c == ';' || c == '=' || c == '+' || c == '-'
                || c == '*' || c == '/' || c == ':' || c == '<' || c == '>')
            {
                ungetNextChar();
                save = FALSE;
                state = DONE;
                currentToken = NUM;
            }
            break;

            // if (!isdigit(c))
            // {
            //     ungetNextChar();
            //     save = FALSE;
            //     state = DONE;
            //     currentToken = NUM;
            // }
        // 处理标识符
        case INID:
            // 空白字符分割标识符 或 遇到运算符号
            if (c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == EOF 
                || c == ',' || c == ';' || c == '=' || c == '+' || c == '-'
                || c == '*' || c == '/' || c == ':' || c == '<' || c == '>')
            {
                ungetNextChar();
                save = FALSE;
                state = DONE;
                currentToken = ID;
            }
            break;

            // if (!isalpha(c) && !isdigit(c))
            // {
            //     ungetNextChar();
            //     save = FALSE;
            //     state = DONE;
            //     currentToken = ID;
            // }
        case DONE:
        default: /* 不应该发生 */
            fprintf(listing, "词法分析器错误: 状态= %d\n", state);
            state = DONE;
            currentToken = ERROR;
            break;
        }
        if ((save) && (tokenStringIndex <= MAXTOKENLEN))
            tokenString[tokenStringIndex++] = (char)c;
        if (state == DONE)
        {
            tokenString[tokenStringIndex] = '\0';
            if (currentToken == ID)
                currentToken = reservedLookup(tokenString);
        }
    }

    if (TraceScan)
    {
        fprintf(listing, "\t%d: ", lineno);
        printToken(currentToken, tokenString);
    }
    return currentToken;
} /* end getToken */