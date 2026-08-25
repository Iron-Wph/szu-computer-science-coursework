# LR(0) DFA 状态图

这个图表展示了LR(0)语法分析的DFA状态转换图。每个状态包含其项目集，箭头表示状态之间的转换及其对应的符号。

```mermaid
stateDiagram-v2
    0: "State 0<br/>S' -> .E<br/>E -> .E+T<br/>E -> .T<br/>T -> .T*F<br/>T -> .F<br/>F -> .(E)<br/>F -> .i"
    1: "State 1<br/>S' -> E.<br/>E -> E.+T"
    2: "State 2<br/>E -> T.<br/>T -> T.*F"
    3: "State 3<br/>T -> F."
    4: "State 4<br/>F -> (.E)<br/>E -> .E+T<br/>E -> .T<br/>T -> .T*F<br/>T -> .F<br/>F -> .(E)<br/>F -> .i"
    5: "State 5<br/>F -> i."
    6: "State 6<br/>E -> E+.T<br/>T -> .T*F<br/>T -> .F<br/>F -> .(E)<br/>F -> .i"
    7: "State 7<br/>T -> T*.F<br/>F -> .(E)<br/>F -> .i"
    8: "State 8<br/>F -> (E.)<br/>E -> E.+T"
    9: "State 9<br/>E -> E+T.<br/>T -> T.*F"
    10: "State 10<br/>T -> T*F."
    11: "State 11<br/>F -> (E)."
    0 --> 1: "E"
    0 --> 2: "T"
    0 --> 3: "F"
    0 --> 4: "("
    0 --> 5: "i"
    1 --> 6: "+"
    2 --> 7: "*"
    4 --> 8: "E"
    4 --> 2: "T"
    4 --> 3: "F"
    4 --> 4: "("
    4 --> 5: "i"
    6 --> 9: "T"
    6 --> 3: "F"
    6 --> 4: "("
    6 --> 5: "i"
    7 --> 10: "F"
    7 --> 4: "("
    7 --> 5: "i"
    8 --> 11: ")"
    8 --> 6: "+"
    9 --> 7: "*"
```

## 状态说明

- State 0: 初始状态，包含所有以点号开始的项目
- State 1: 接受状态 S' -> E. 和等待加法操作的状态
- State 2: 完成项 E -> T. 和等待乘法操作的状态
- State 3: 完成项 T -> F.
- State 4: 左括号状态，包含新的嵌套表达式开始
- State 5: 标识符完成状态
- State 6: 加法操作后等待T的状态
- State 7: 乘法操作后等待F的状态
- State 8: 括号内表达式完成，等待右括号或加法
- State 9: 加法完成后等待乘法的状态
- State 10: 乘法完成状态
- State 11: 括号表达式完成状态