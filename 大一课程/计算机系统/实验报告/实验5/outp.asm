.ORIG x3000
LD R6, stack;;;;栈指针初始化
;;;;;
LD R1,vec   ;set up the keyboard interrupt vector table entry
LD R2,rupt
STR R2,R1,#0;;;;;;;修改该x0180调用号的内容
;;;;;
;;;;;;;中断标志置位,标志位首先为0就不需要考虑进位
LD R4,IE
NOT R4,R4;;;;;;X4000取非
LDI R3,KBSR;;;;;标志位置位1
NOT R3,R3
AND R3,R3,R4
NOT R3,R3;;;;;;;;R3取非后就已经修改置位
STI R3,KBSR
;;;;;
;;;;;
show JSR DELAY;;;;先进行延迟，再进行输出，以下为输出程序
;;;;;输出分为两行依次输出，第一行的输出
     AND R1,R1,#0
     ADD R1,R1,#-6
ag   LEA R0,ics1
     TRAP X22    
     ADD R1,R1,#1
     BRnp  ag
     LD R0,hang    ;;;;;输出换行
     TRAP X21
     BRnzp sec
;;;;;
;;;第二行输出
;;;;;
sec  AND R1,R1,#0
     ADD R1,R1,#-5
aga  LEA R0,ics2
     TRAP X22  
     ADD R1,R1,#1
     BRnp  aga
     LD R0,hang    ;;;;;输出换行
     TRAP X21
     BRnzp show
     HALT
;;
;;
vec .fill x0180
rupt .fill x2000
IE .fill x4000
KBSR .fill xFE00


stack .fill x3000
ics1 .stringz "ICS     "
ics2 .stringz "     ICS";;;;;;5个空格
hang .fill #10
;;;;子程序delay
DELAY   ST  R1, SaveR1
        LD  R1, COUNT
REP     ADD R1,R1,#-1
        BRp REP
        LD  R1, SaveR1
        RET
COUNT   .FILL x4000
SaveR1  .BLKW 1
;;;;
.END