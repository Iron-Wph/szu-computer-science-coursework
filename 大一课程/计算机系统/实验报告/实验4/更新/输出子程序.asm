;;;;;;;;输出子程序
;
;
;
;
;
;
output LD R7,saveR7;使用了trap输出。需要保存R7
       LD R0,saveR0;trap输出需要初始化R0
       LD R1,saveR1;R1作为循环计数器从0-35,
       LD R2,saveR2;R2作为控制空格或者换行符的输出，从5开始到35；
       LD R3,saveR3
       LD R4,saveR4
       LD R5,saveR5
       LD R6,saveR6
;保存区
    LEA R6,pan
    ADD R2,R2,#5;R2初始化为5
    AND R1,R1,#0;
;
;loop开始
;
loop  LD R3,length
      ADD R3,R3,R1;R3=R1+length
      BRz done;若R3为0，则结束输出
      ADD R6,R6,R1;R0=R6+R1,获取增量位置输出
;输出
      LDR R4,R6,#0;直接取出棋盘上对应位置的数据，再进行判断
      BRp p1 
      BRn p2
;无跳转，则直接输出空白
      LD R0,bai
      BRnzp out
;输出play1
p1    LD R0,play1
      BRnzp out
;输出play2
p2    LD R0,play2
;
out TRAP X21;输出棋盘的字符
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
      ST R7,saveR7
      ST R0,saveR0
      ST R1,saveR1
      ST R2,saveR2
      ST R3,saveR3
      ST R4,saveR4
      ST R5,saveR5
      ST R6,saveR6
;恢复区
done  ret;
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