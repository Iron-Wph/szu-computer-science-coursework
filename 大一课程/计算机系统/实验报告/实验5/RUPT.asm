.ORIG X2000
ST R0,SR0
ST R1,SR1
ST R2,SR2
ST R3,SR3
ST R4,SR4
ST R7,SR7
;;;;;;
LD R2,hang;;;;;;R2初始化为行，用于判断输入是否结束
LEA R3,data
;;;;;;
START LDI R1,KBSR 
      BRzp START
      LDI R0,KBDR    
;;;;;get it and write 
;;;;回显后再存入
ECHO  LDI R1,DSR
      BRzp ECHO
      STI R0,DDR
;;;;;存入数据
      ADD R4,R0,R2
      BRz next
      STR R0,R3,#0
      ADD R3,R3,#1
      BRnzp START 
;;;;;
next AND R4,R4,#0
     ADD R4,R4,#-10
     LEA R0,data
aga  JSR show;;;;;;调用我写的show子程序输出字符串
     ADD R4,R4,#1
     BRz done
     BRnzp aga
;;;;;数据恢复区
done LD R0,SR0
     LD R1,SR1
     LD R2,SR2
     LD R3,SR3
     LD R4,SR4
     LD R7,SR7
     RTI
;;;;;DATA AREA
SR0 .FILL #0
SR1 .FILL #0
SR2 .FILL #0
SR3 .FILL #0
SR4 .FILL #0
SR7 .FILL #0
hang .fill #-10
data .blkw #100
KBSR .FILL XFE00
KBDR .FILL XFE02
DSR .FILL XFE04
DDR .FILL XFE06
;;;;;
;;;;;
;;;;;
;;;;;子程序show
show ST R7,SAVER7
     ST R0,SAVER0
     ST R1,SAVER1
     ST R3,SAVER3
;;;;
LOOP LDR R1,R0,#0
     BRz return 
L2   LDI R3,DSR
     BRzp L2
     STI R1,DDR
     ADD R0,R0,#1
     BRnzp LOOP
;;;;;
return LD R3,SAVER3 
       LD R1,SAVER1 
       LD R0,SAVER0 
       LD R7,SAVER7 
     RET
;;;
SAVER0 .FILL #0
SAVER1 .FILL #0
SAVER3 .FILL #0
SAVER7 .FILL #0
;;;;;;;
;;;;;;;
;;;;;;;
.END