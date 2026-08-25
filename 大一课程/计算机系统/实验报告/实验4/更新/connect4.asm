.ORIG x3000
;构建棋盘，从0-35，将输入列号依次+29后依次递减，若该列放满    则输出错误信息
;
    LEA R6,pan;;;;;;;;;;R6存放棋盘的首地址
    JSR output;输出空棋盘
    AND R1,R1,#0;
    ADD R1,R1,#1;R1初始化为1
    AND R2,R2,#0
    AND R3,R3,#0;
    LD R3,length;;;;;R3初始化为-36，记录次数，判断是否平局
    

;
;
;循环开始，哨兵法（在判断中返回值判断是否结束）
xuan AND R1,R1,#1;相与后的结果来判断执行哪个选手下棋，若为0，则为选手2；若为1，则为选手1
     JSR input
     JSR output
     JSR ext  
     ADD R2,R2,#0
     BRp victory
     AND R2,R2,#0
     ADD R3,R3,#1;;;;调用次数加1
     BRz equal
     ADD R1,R1,#1;;;;;;;;;;R1++
     BR xuan
;;;;;
;;;;;
equal LEA R0,ping;;;;;;输出平局     
      TRAP X22;
      BR bye
;;;;;;
victory ADD R1,R1,#0
        BRp vv
        LEA R0,win2
        BR py
vv      LEA R0,win1
py      TRAP X22;
;;;;
;;;;
;;;;
bye     HALT;程序终止
;;;
pan .blkw 36 #0
length .fill #-36;用于数据输出的判断
;;;
;下列数据使用puts输出
in1 .stringz "Player 1, choose a column: "
in2 .stringz "Player 2, choose a column: "
eroor .stringz "Invalid move.Try again.\n"
win1 .stringz "Player 1 Wins."
win2 .stringz "Player 2 Wins."
ping .stringz "Tie Game."


;
;
;
;输入子程序，入口参数为R1，传给R6，用于决定选手1或2的操作
;保存区
input  ST R7,save7
       ST R0,save0
       ST R1,save1
       ST R2,save2
       ST R3,save3
       ST R4,save4
       ST R5,save5
       ST R6,save6

;处理区
      ADD R6,R1,#0;;;;;之后的使用不修改R6
over  ADD R6,R6,#0
      BRz change
      LEA R0,in1
      BRnzp display
change   LEA R0,in2
display  TRAP X22;提示输入信息
         AND R1,R1,#0;
         LD R1,hao;R1初始化为#-48，用于判断输入字符的范围1-6
;
;
;
;输入
;
;
    TRAP X23;;;;;;;;;;;;获取输入
    ADD R2,R0,#0;;;;;;;;;;;;R2为输入的字符的ASCII码  
    ADD R2,R2,R1;;;;;;;;;;;;将字符转化为数字
    BRp k;如果大于0则满足大于等于1
    BRnzp  undeny ;跳到不合条件部分处理
k   ADD R2,R2,#-6;;;;;;;判断是否小于等于6
    BRp undeny;
;
;列号正确后的处理，判断是否放满，若满则输出错误
;    
    ADD R2,R2,#6;;;;;;;;R2恢复为输入列号
    LD R1,yi;;;;;R1==#29
    ADD R2,R2,R1;;;;;;;;pan首地址加R2获得相应地址
    ADD R3,R3,#6;;;;R3==6,作为循环计数，若为0，则输出错误信息
dd  BRz undeny
    LEA R4,pan
    ADD R4,R4,R2;获取当前地址
    LDR R5,R4,#0;;;;;;;;;对应位置为0就写入
    BRz xie
    ADD R2,R2,#-6
    ADD R3,R3,#-1
    BRnzp dd
xie ADD R6,R6,#0;;;判断哪位选手的输入，填入相应的数值
    BRz ko
    STR R6,R4,#0
    BR CUN
ko  ADD R6,R6,#-1;;;;;R6=-1再进行赋值
    STR R6,R4,#0
    BR CUN
;
;
undeny  LEA R0,eroor
        TRAP X22
        BRnzp over;;;;;;;输入为错误信息，则重新执行over开始的输入   

;恢复区
CUN    LD R7,save7
       LD R0,save0
       LD R1,save1
       LD R2,save2
       LD R3,save3;
       LD R4,save4
       LD R5,save5
       LD R6,save6    

   RET;
yi .fill #29
hao .fill #-48
save7 .fill 0
save0 .fill 0
save1 .fill 0
save2 .fill 0
save3 .fill 0
save4 .fill 0
save5 .fill 0
save6 .fill 0
;;;;;
;;;;;用于超出判断子程序的内存访问
;;;;;
tplace  .fill x31D3
beg  .fill #35
saR0 .fill #0
saR1 .fill #0
saR3 .fill #0
saR4 .fill #0
saR5 .fill #0
saR6 .fill #0
saR7 .fill #0
;
;
;
;
;
;
;
;
;;;;;判断是否为结束,入口参数为R1，返回值为R2;;;;;;;;;;;;;;;;;变量地址待修改;;;;;;;;;;;
;;;保存区
ext  ST R7,saR7
     ST R0,saR0
     ST R1,saR1
     ST R3,saR3
     ST R4,saR4
     ST R5,saR5
     ST R6,saR6
;;;;;;;;;;;;;;;;;
;;;;;根据R1的值判断选手，对应判断
     LD R0,beg;;;;R0初始化为35，作为循环计数器
     AND R2,R2,#0
     LEA R4,pan
;;;;;;;;;选手1
;;;行
chu   AND R7,R7,#0
      ADD R7,R7,#5;;;;;;R7作为内层循环计数器
      AND R5,R5,#0
      AND R3,R3,#0
      ADD R3,R4,R0;;;;;R3计算相应的地址
tin   LDR R1,R3,#0;;;;;数据给R1
      STI R3,tplace           ;;;;;;PC增量限制，间接寻址，需要判断哪位选手在操作就先暂存R3的内容

      LD R3,saR1
      BRz ww2;;;;;;为0则为选手2，否则为选手1
      LDI R3,tplace
      ADD R1,R1,#-1
      BRnzp tww
ww2   LDI R3,tplace
      ADD R1,R1,#1

tww   BRz RR;;;;;;;;;;R5++,若R5为#4则说明结束
      AND R5,R5,#0
      BRnzp R
RR    ADD R5,R5,#1
R     ADD R6,R5,#-4;
      BRn hh
      ADD R2,R2,#1
      BRnzp exit

hh    ADD R7,R7,#-1 ;;;地址只会加或减5次
      BRn  jj
      ADD R3,R3,#-1;;;;;R3偏移
      BRnzp tin
jj    ADD R0,R0,#-6;;;;;R0-6，往上一行
      BRn LLL;;;;;;;;;跳去下一种判断
      BRnzp chu
;;;;;;;;
;;;;列
;;;;; 
LLL   AND R0,R0,#0
      ADD R0,R0,#5
      AND R5,R5,#0
lc    AND R7,R7,#0
      ADD R7,R7,#5
      ADD R3,R4,R0;;;;;;R3存放地址
agg   LDR R1,R3,#0
      STI R3,tplace
      LD R3,saR1

      BRz ttw
      LDI R3,tplace
      ADD R1,R1,#-1
      BRnzp tji
ttw   LDI R3,tplace
      ADD R1,R1,#1

tji   BRz LL;;;;;;;;;;R5++,若R5为#4则说明结束
      AND R5,R5,#0
      BRnzp QQ
LL    ADD R5,R5,#1
QQ    ADD R6,R5,#-4;
      BRn GG
      ADD R2,R2,#1
      BRnzp exit

GG    ADD R7,R7,#-1 
      BRn  nn
      ADD R3,R3,#6;;;;;R3偏移
      BRnzp agg
nn    ADD R0,R0,#-1;;;;;R0-1，往上一列
      BRn zhu;;;;;;;;;跳去下一种判断
      BRnzp lc   
        
;;;;;;;
;;;;;;;主对角线
;;;;;;;
zhu   AND R0,R0,#0
      AND R5,R5,#0
      AND R7,R7,#0
ee    ADD R7,R7,#6
      ADD R1,R0,#-2;;;;;判断是否走完0，1，2
      BRz KK
      BRp MM;;;;;;;;;;;此步已完成0，1，2，则跳到6和12
KK    ADD R3,R4,R0;;;;;;;;;;;;;R3获得增量地址
ag    LDR R1,R3,#0;;;;;;;;;;;;;R1对应位置的内容
      ST R3,place
      LD R3,saR1
      BRz xx2
      LD R3,place
      ADD R1,R1,#-1
      BRnzp jji
xx2   LD R3,place
      ADD R1,R1,#1
jji   BRz p
      AND R5,R5,#0
      BRnzp Q
p     ADD R5,R5,#1
Q     ADD R6,R5,#-4;
      BRn XX 
      ADD R2,R2,#1
      BRnzp exit 
 
XX    ADD R7,R7,#-1          
      BRz  nnn
      ADD R3,R3,#7;;;;;R3偏移
      BRnzp ag
nnn   ADD R0,R0,#1
      ADD R7,R7,#-1
      BRnzp ee
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;6和12
MM    AND R0,R0,#0
      ADD R0,R0,#6
;;
      AND R5,R5,#0
      AND R7,R7,#0
eee   ADD R7,R7,#4
      ADD R1,R0,#-12
      BRp fu;;;;;;;;;;;主对角线判断完，则跳到副对角线
      ADD R3,R4,R0
aga   LDR R1,R3,#0
      ST R3,place
      LDI R3,tsaR1
      BRz tx2
      LD R3,place
      ADD R1,R1,#-1
      BRnzp jjt
tx2   LD R3,place
      ADD R1,R1,#1
jjt   BRz pa
      AND R5,R5,#0
      BRnzp Qa
pa    ADD R5,R5,#1
Qa    ADD R6,R5,#-4;
      BRn XXa 
      ADD R2,R2,#1
      BRnzp exit 
 
XXa   ADD R7,R7,#-1          
      BRz  wwnn
      ADD R3,R3,#7;;;;;R3偏移
      BRnzp aga
wwnn  ADD R0,R0,#6
      ADD R7,R7,#-1
      BRnzp eee      
;;;;;;;
;;;;;;;
;;;;;;;副对角线
;;;;;;;
;;;;;;;
fu    AND R0,R0,#0
      AND R5,R5,#0
      AND R7,R7,#0
      ADD R0,R0,#5
we    ADD R7,R7,#6
      ADD R1,R0,#-3
      BRz tt
      BRn tm;;;;;;;;;;;此步已完成3，4，5，则跳到11和17
tt    ADD R3,R4,R0
tgg   LDR R1,R3,#0
      ST R3,place
      LDI R3,tsaR1
      BRz wx2
      LD R3,place
      ADD R1,R1,#-1
      BRnzp jjw
wx2   LD R3,place
      ADD R1,R1,#1
jjw   BRz ppp
      AND R5,R5,#0
      BRnzp qqq
ppp   ADD R5,R5,#1
qqq   ADD R6,R5,#-4;
      BRn tx 
      ADD R2,R2,#1
      BRnzp exit 
 
tx    ADD R7,R7,#-1          
      BRz  tn
      ADD R3,R3,#5;;;;;R3偏移,副对角线为+5
      BRnzp tgg
tn    ADD R0,R0,#-1
      ADD R7,R7,#-1
      BRnzp we
;;;;;;;;;;;;;;;;;;;;;;11和17
tm    AND R0,R0,#0
      ADD R0,R0,#11
;;
      AND R5,R5,#0
      AND R7,R7,#0
tee   ADD R7,R7,#4
      ADD R1,R0,#-16
      ADD R1,R1,#-1;;;;;;;;R1-17,判断是否结束
      BRp exit;;;;;;;;;;
      ADD R3,R4,R0
gga   LDR R1,R3,#0
      ST R3,place
      LDI R3,tsaR1
      BRz ss2
      LD R3,place
      ADD R1,R1,#-1
      BRnzp jjs
ss2   LD R3,place
      ADD R1,R1,#1
jjs   BRz paa
      AND R5,R5,#0
      BRnzp Qaa
paa   ADD R5,R5,#1
Qaa   ADD R6,R5,#-4;
      BRn ssa 
      ADD R2,R2,#1
      BRnzp exit 
 
ssa   ADD R7,R7,#-1          
      BRz  wn
      ADD R3,R3,#5;;;;;R3偏移
      BRnzp gga
wn    ADD R0,R0,#6
      ADD R7,R7,#-1
      BRnzp tee  
;;;;;;;;;;;;;;;;;    
;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;
;;;恢复区
exit LDI R7,tsaR7
     LDI R0,tsaR0
     LDI R1,tsaR1
     LDI R3,tsaR3
     LDI R4,tsaR4
     LDI R5,tsaR5
     LDI R6,tsaR6
;;;;;;    
     RET
;
;
;
place .fill #0
tsaR0 .fill x30FD
tsaR1 .fill x30FE
tsaR3 .fill x31FF
tsaR4 .fill x3100
tsaR5 .fill x3101
tsaR6 .fill x3102
tsaR7 .fill x3103
;;;;;;
;;;;;;;;输出子程序
;无返回值，无需入口参数
;
;
;
;
;
output ST R7,saveR7;使用了trap输出。需要保存R7
       ST R0,saveR0;trap输出需要初始化R0
       ST R1,saveR1;R1作为循环计数器从0-35,
       ST R2,saveR2;R2作为控制空格或者换行符的输出，从5开始到35；
       ST R3,saveR3
       ST R4,saveR4
       ST R5,saveR5
       ST R6,saveR6
;保存区
    AND R2,R2,#0
    ADD R2,R2,#5;R2初始化为5
    AND R1,R1,#0;
;
;loop开始
;
loop  LD R6,saveR6
      LD R3,tlength
      ADD R3,R3,R1;R3=R1+tlength
      BRz done;若R3为0，则结束输出
      ADD R6,R6,R1;R0=R6+R1,获取增量位置输出
;输出
      LDR R4,R6,#0;直接取出棋盘上对应位置的数据，再进行判断
      BRp p1
      ADD R4,R4,#0
      BRn p2
;无跳转，则直接输出空白
      LD R0,bai
      BRnzp show
;输出play1
p1    LD R0,play1
      BRnzp show
;输出play2
p2    LD R0,play2
;
show  TRAP X21;输出棋盘的字符
;
;
;输出换行或者空格
       ADD R5,R2,#0
       NOT R5,R5
       ADD R5,R5,#1;R5=-R2
       ADD R3,R1,R5;R3=R1+R5，若为0则输出换行
       BRz  huan
       LD R0,kong
       BRnzp again
huan   ADD R2,R2,#6
       LD R0,hang
 
again  TRAP X21
;
;两种输出结束后回到循环开始
       ADD R1,R1,#1
       BRnzp loop
;
;输出区
done  LD R7,saveR7
      LD R0,saveR0
      LD R1,saveR1
      LD R2,saveR2
      LD R3,saveR3
      LD R4,saveR4
      LD R5,saveR5
      LD R6,saveR6
;恢复区
      RET;
;
;
;
tlength .fill #-36
saveR7 .fill 0
saveR0 .fill 0
saveR1 .fill 0
saveR2 .fill 0
saveR3 .fill 0
saveR4 .fill 0
saveR5 .fill 0
saveR6 .fill 0
kong .fill #32
hang .fill #10
play1 .fill x004F
play2 .fill x0058
bai .fill x002D
;
;
;
;
;
;
;
;
;
.END