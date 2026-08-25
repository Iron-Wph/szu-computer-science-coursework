// 实现基本的shell功能
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <signal.h>
#include <errno.h>
#include <time.h>
#include <unistd.h>
void handle_pipe_command(char *line);
void handle_redirection(char **args);
int handle_config(char *command, char **args);

int main(){
    char current_dir[1024]; // 存储PWD获取的当前目录
    // 通过pwd指令获取路径
    if(getcwd(current_dir,sizeof(current_dir)) == NULL)
        perror("getcwd");

    printf("Hello Wph@shell:~%s\n", current_dir);

    char line[1024];    // 存储命令行输入
    
    // 预先保存标准输入输出，使得及时恢复
    int out = dup(STDOUT_FILENO); // 保存标准输出
    int in = dup(STDIN_FILENO);   // 保存标准输入

    while(1){
        // 通过pwd指令获取路径
        if(getcwd(current_dir,sizeof(current_dir)) == NULL)
            perror("getcwd");
        
        printf("\033[1;32m%s\033[0m:\033[1;34m~%s>\033[0m", "Wph@shell",current_dir);
        if(fgets(line, sizeof(line), stdin) == NULL)
        {
            // 输入错误
            break;
        }
        // 去掉换行符
        line[strcspn(line, "\n")] = 0;

        // 判断是否为管道命令
        if (strchr(line, '|') != NULL) 
        {
            handle_pipe_command(line);
        }
        // 非管道命令则直接执行
        else
        {
            // 解析命令行，根据空格和制表符分割参数
            char *args[100];    // 存储命令行参数
            int flag = handle_config(line, args);
            handle_redirection(args);
            // 内部命令执行
            if(flag == 1){
                // 内部命令
                if(args[1] != NULL && strcmp(args[2], "exit") == 0){
                    exit(0);
                }
                else if (args[1] != NULL && strcmp(args[2], "cd") == 0){
                    // printf("进入的m目录为%s\n", args[3]);
                    if(args[3] == NULL){
                        char *home_dir = getenv("HOME");
                        if (home_dir == NULL) {
                            // 如果无法获取主目录路径，输出错误信息
                            perror("无法获取主目录路径");
                            return -1;
                        }
                        chdir(home_dir);
                    }
                    else if(strcmp(args[3], "-") == 0){
                        // 用 .. 去模拟
                        chdir("..");
                    }
                    else{
                        chdir(args[3]);
                    }
                }
                // 内部命令和系统命令通过fork子进程执行
                else{
                    // 创建子进程
                    int pid = fork();
                    if (pid == -1){
                        perror("fork");
                        exit(1);
                    }
                    else if(pid == 0){
                        // 子进程执行命令
                        if(execvp(args[0], args) == -1){
                            // 无效命令
                            printf("无效命令: %s\n", args[0]);
                            exit(1);
                        }
                        printf("子进程已经完成\n");
                        exit(0);
                    }
                    else{
                        // 父进程等待子进程结束
                        waitpid(pid, NULL, 0);
                        dup2(out, STDOUT_FILENO); // 恢复标准输出
                        dup2(in, STDIN_FILENO);   // 恢复标准输入
                    }
                }
            }
            // 外部命令执行
            else{
                // 如果输入不是系统命令且没有 "./" 则手动加上路径
                if(strncmp(args[0], "./", 2) != 0){
                    char new_str[100];
                    strcpy(new_str, "./");
                    strcat(new_str, args[0]);
                    strcpy(args[0], new_str);                    
                }
                // 创建子进程
                int pid = fork();
                if (pid == -1){
                    perror("fork");
                    exit(1);
                }
                else if(pid == 0){
                    // 子进程执行命令
                    if(execvp(args[0], args) == -1){
                        // 无效命令
                        printf("无效命令: %s\n", args[0]);
                        exit(1);
                    }
                    printf("子进程已经完成\n");
                    exit(0);
                }
                else{
                    // 父进程等待子进程结束
                    waitpid(pid, NULL, 0);
                    dup2(out, STDOUT_FILENO); // 恢复标准输出
                    dup2(in, STDIN_FILENO);   // 恢复标准输入
                }
            }
        }
    }
    return 0;
}

// 判断是否是内部命令
int is_builtin_command(const char *cmd) {
    char command[256] = {0};
    snprintf(command, sizeof(command), "/bin/bash -c 'type -t %s'", cmd);
    FILE *fp = popen(command, "r");
    if (fp == NULL) {
        perror("popen");
        return -1;
    }
    char result[32] = {0};
    if (fgets(result, sizeof(result), fp) == NULL) {
        perror("fgets");
        pclose(fp);
        return -1;
    }
    pclose(fp);
    // 去除末尾换行符
    size_t len = strlen(result);
    if (len > 0 && result[len - 1] == '\n') 
        result[len - 1] = '\0';

    if(strncmp(result, "builtin", 7) == 0 )
        return 1;
    else if(strncmp(result, "file", 4) == 0)
        return 2;
    else
        return 0;
}

// 处理管道命令 
void handle_pipe_command(char*line){
    char *command[2];
    char *token = strtok(line, "|");
    int i = 0;
    while(token != NULL && i < 2){
        command[i++] = token;
        token = strtok(NULL, "|");
    }
    // 确保传入两个命令
    if(i == 2){
        int pid1, pid2;
        // 创建管道
        int fds[2];
        if(pipe(fds) == -1){
            perror("pipe");
            exit(1);
        }
        // 创建第一个子进程
        pid1 = fork();
        if(pid1 == -1){
            perror("fork");
            exit(1);
        }
        else if(pid1 == 0){
            // 关闭读端
            close(fds[0]);
            // 将标准输出重定向到写端
            dup2(fds[1], STDOUT_FILENO);
            // 关闭原来的写端
            close(fds[1]);
            // 提取参数
            char *args[100];
            handle_config(command[0], args);
            // 重定向操作
            handle_redirection(args);
            // 替换为相应的进程
            if(execvp(args[0], args) == -1)
            {
                // 程序出错
                perror("execvp");
                exit(1);
            }
        }
        else{
            // 创建第二个子进程
            pid2 = fork();
            if(pid2 == -1){
                perror("fork");
                exit(1);
            }
            else if(pid2 == 0){
                // 关闭原来的写端
                close(fds[1]);
                // 将标准输入重定向到读端
                dup2(fds[0], STDIN_FILENO);
                // 关闭读端
                close(fds[0]);
                // 提取参数
                char *args[100];
                handle_config(command[1], args);
                // 重定向操作
                handle_redirection(args);
                // 替换为相应的进程
                if(execvp(args[0], args) == -1)
                {
                    // 程序出错
                    perror("execvp");
                    exit(1);
                }
            }
            // 关闭所有子进程，避免出现僵尸或孤儿进程
            else
            {
                // 父进程关闭管道
                close(fds[0]);
                close(fds[1]);
                // 等待子进程结束
                waitpid(pid1, NULL, 0);
                waitpid(pid2, NULL, 0);
            }
        }
    }
}

// 重定向操作
void handle_redirection(char **args){
    for (int i=0;args[i]!= NULL;i++){
        if(strcmp(args[i], ">") == 0){
            int fd = open(args[i+1], O_WRONLY | O_CREAT | O_TRUNC, 0666);
            dup2(fd, STDOUT_FILENO);
            close(fd);
            args[i] = NULL; // 将重定向符号和文件名替换为NULL
            break;
        }
        else if(strcmp(args[i], ">>") == 0){
            int fd = open(args[i+1], O_WRONLY | O_CREAT | O_APPEND, 0666);
            dup2(fd, STDOUT_FILENO);
            close(fd);
            args[i] = NULL; // 将重定向符号和文件名替换为NULL
            break;
        }
        else if(strcmp(args[i], "<") == 0){
            int fd = open(args[i+1], O_RDONLY);
            dup2(fd, STDIN_FILENO);
            close(fd);
            args[i] = NULL; // 将重定向符号和文件名替换为NULL
            break;
        }
    }
}

// 处理参数
int handle_config(char *command, char **args){
    // 提取参数
    command = strtok(command, " \t\n");
    int i = 0;
    int flag = 0;       // 是否为内部或系统命令的标志
    if(is_builtin_command(command) == 1){
        args[i++] = "/bin/bash";
        args[i++] = "-c";
        flag = 1;
    }
    else if(is_builtin_command(command) == 2){
        flag = 1;
    }

    while(command != NULL){
        args[i++] = command;
        command = strtok(NULL, " \t\n");
    }
    args[i] = NULL; // 添加结束符
    return flag;
}