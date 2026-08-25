.orig x3000;程序初始位置为x3000
;
;
;冒泡排序
    AND R0,R0,#0;R0 为第一个循环计数
    ADD R0,R0,#1;R0==1
    AND R1,R1,#0;R1==0 为第二个循环计数
;第一个循环
PA  ADD R2,R0,#-16;计算j-n
    BRZ CUN;当R2==0时，跳出排序      
; 
;第二个循环
PB  ADD R3,R1,R0;
    ADD R3,R3,#-16;计算k-n+j
    BRZ JA;当R3==0时，跳出循环,,,跳到第一个循环的计数
;
;第一个循环开始
;标号为num的值为x3200，用寄存器R4存储其地址
    LD R4,num;
    ADD R4,R4,R1;以下两步访问num[R1]
    LDR R5,R4,#0;R5=num[R1]
;
    ADD R4,R4,#1;以下两步访问num[R1++]
    LDR R6,R4,#0;R6=num[R1++]
;
;算法判断if(num[R1]<num[R1++]) 用R7=R5-R6<0 后面需要存数就不修改R4,保持R4不变
    NOT R7,R6;
    ADD R7,R7,#1;R7=-R6
    ADD R7,R5,R7;完成R7=R5-R6
    BRzp  JB;判断是否符合交换条件
;不符合就跳出交换和存数>>>>>跳到JB          即>=0
;
;交换代码 用R7交换寄存器R5与R6
    AND R7,R7,#0;R7清零
    ADD R7,R5,#0;R7=R5
    ADD R5,R6,#0;R5=R6
    ADD R6,R7,#0;R6=R7,完成交换
;将交换后的数存回对应位置
    STR R6,R4,#0;R6=num[R1++]
    STR R5,R4,#-1;R5=num[R1]
    
;
;
JB  ADD R1,R1,#1; R1++;
    BRnzp PB;跳回第二个循环判断
JA  AND R1,R1,#0;R1清零
    ADD R0,R0,#1;排序最后 R0++
    BRnzp PA;跳回第一个循环判断
;
;
;
;
;
;给个循环存数在x4000处
;
CUN AND R0,R0,#0;R0清零,R0为16则跳出循环
    AND R1,R1,#0;R1清零
    LD R1,mark;R1存放数据保存首地址，R4仍为数据初始地址num
    LD R4,num;
;
CON ADD R5,R4,R0;
    LDR R2,R5,#0;R2==num[R0];
    ADD R6,R1,R0;
    STR R2,R6,#0;写入数据
    ADD R0,R0,#1;R0++;
    ADD R3,R0,#-16;
    BRn CON;
; 
;
;计算A等级
;courtA 
      AND R0,R0,#0;R0清零
      AND R5,R5,#0;R5清零
      LD R1,GA;
couA  ADD R2,R4,R0;R2用于地址变化
      LDR R3,R2,#0;
      ADD R3,R3,R1;
      BRn #1;
      ADD R5,R5,#1;R5++计算A等级个数
      ADD R0,R0,#1;
      ADD R6,R0,#-4;
      BRn couA;
;
;A等级个数存入LA
      STI R5,LA;
;
;
;计算B等级
;courtB 
      AND R0,R0,#0
      ADD R0,R0,R5;
      AND R5,R5,#0
      LD R1,GB;
couB  ADD R2,R4,R0;R2用于地址变化
      LDR R3,R2,#0;
      ADD R3,R3,R1;
      BRn #1;
      ADD R5,R5,#1;R5++计算B等级个数
      ADD R0,R0,#1;
      ADD R6,R0,#-8;
      BRn couB;
;
;B等级个数存入LB
      STI R5,LB;
;
;   


halt;
num .fill x3200
mark .fill x4000
LA .fill x4100
LB .fill x4101
GA .fill #-85
GB .fill #-75

.end