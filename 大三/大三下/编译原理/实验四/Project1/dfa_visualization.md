# DFA State Diagram Visualization

This diagram shows the DFA states and their transitions for the grammar. Each state contains its item set, and transitions are labeled with their corresponding symbols.

```mermaid
graph LR
    0["State 0<br/>S' -> .E<br/>E -> .E+T<br/>E -> .T<br/>T -> .T*F<br/>T -> .F<br/>F -> .(E)<br/>F -> .i"]
    1["State 1<br/>S' -> E.<br/>E -> E.+T"]
    2["State 2<br/>E -> T.<br/>T -> T.*F"]
    3["State 3<br/>T -> F."]
    4["State 4<br/>F -> (.E)<br/>E -> .E+T<br/>E -> .T<br/>T -> .T*F<br/>T -> .F<br/>F -> .(E)<br/>F -> .i"]
    5["State 5<br/>F -> i."]
    6["State 6<br/>E -> E+.T<br/>T -> .T*F<br/>T -> .F<br/>F -> .(E)<br/>F -> .i"]
    7["State 7<br/>T -> T*.F<br/>F -> .(E)<br/>F -> .i"]
    8["State 8<br/>F -> (E.)<br/>E -> E.+T"]
    9["State 9<br/>E -> E+T.<br/>T -> T.*F"]
    10["State 10<br/>T -> T*F."]
    11["State 11<br/>F -> (E)."]
    
    0 -->|"("| 4
    0 -->|"E"| 1
    0 -->|"F"| 3
    0 -->|"T"| 2
    0 -->|"i"| 5
    
    1 -->|"+"| 6
    
    2 -->|"*"| 7
    
    4 -->|"("| 4
    4 -->|"E"| 8
    4 -->|"F"| 3
    4 -->|"T"| 2
    4 -->|"i"| 5
    
    6 -->|"("| 4
    6 -->|"F"| 3
    6 -->|"T"| 9
    6 -->|"i"| 5
    
    7 -->|"("| 4
    7 -->|"F"| 10
    7 -->|"i"| 5
    
    8 -->|")"| 11
    8 -->|"+"| 6
    
    9 -->|"*"| 7
```

## 说明

该DFA图展示了一个用于解析算术表达式的状态机，包含以下特点：

1. 总共有12个状态（State 0-11）
2. 每个状态包含其项目集（LR(0) items）
3. 状态之间的转换用箭头标注，箭头上的标签表示转换符号
4. 初始状态为State 0
5. 图中展示了所有的产生式和它们在各个状态中的位置

主要的语法规则包括：
- 表达式（E）
- 项（T）
- 因子（F）
- 加法运算（+）
- 乘法运算（*）
- 括号表达式
- 标识符（i） 