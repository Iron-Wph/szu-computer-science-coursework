# f = open("文法2.txt", "rt",encoding="utf-8")

################# 任务一：读取文件 #################
# 打开文法文件
# f = open("Grammar.txt", "rt",encoding="utf-8")
f = open("3_1.txt", "rt",encoding="utf-8")
# 去掉第一行
f.readline()

# 读取四元组的集合
V = f.readline().strip().split(',')     # 非终结符集合
T = f.readline().strip().split(',')     # 终结符集合
P = f.readline().strip().split(',')     # 产生式集合
S = f.readline().strip()                # 起始符号集合

# 输出四元组
print("非终结符：" + " ".join(V))
print("终结符："+" ".join(T))
print("产生式："+" ".join(P))
print("起始符号：" + S)
f.close()


################# 任务二：文法分类 #################
f0 = []             # 存储0型文法
# 遍历所有产生式
for i in range(len(P)):
    # 拆分产生式的左右两边
    ci = P[i].split('->')
    # 判断是否是0型文法
    for j in range(len(V)):
        # 左边包含至少包含一个非终结符
        if ci[0].count(V[j]) != 0:
            f0.append(P[i])
            break
# 去重，转换为集合
f0 = list(set(f0))

epsilon = 'ε'       # 空串
f1 = []             # 存储1型文法
f2 = []             # 存储2型文法
# 判断是否是1型文法
for i in range(len(f0)):
    # 拆分产生式的左右两边
    ci = f0[i].split('->')
    # 在0型的基础上，产生式左边长度小于等于右边
    if len(ci[0]) <= len(ci[1]):
        f1.append(f0[i])
        # 判断是否为2型文法
        if len(ci[0]) == 1:
            # 在1型的基础上，产生式左边长度为1
            f2.append(f0[i])


# 去重，转换为集合
f1 = set(f1)
f2 = set(f2)
f2 = list(f2)
f3 = []             # 存储3型文法
# 在2型文法中找到3型文法
for i in range(len(f2)):
    # 拆分产生式的左右两边
    ci = f2[i].split('->')
    # 右边为终结符串或空串
    all_terminals = True
    w = 0
    for ch in ci[1]:
        if ch not in T and ch != epsilon:
            all_terminals = False
            break
        w += 1          # 保存位置
    if all_terminals:
        # 0表示终结符串或空串
        f3.append((f2[i], 0))
    else:
        # 判断是否为左线性
        if w == 0 and ci[1][0] in V:
            con = True
            for j in range(1, len(ci[1])):
                if ci[1][j] not in T:
                    con = False
                    break
            if con:
                # 1表示左线性文法
                f3.append((f2[i], 1))
        # 判断是否为右线性
        elif w == len(ci[1]) - 1 and ci[1][w] in V:
            con = True
            for j in range(0, len(ci[1]) - 1):
                if ci[1][j] not in T:
                    con = False
                    break
            if con:
                # 2表示右线性文法
                f3.append((f2[i], 2))


f3 = set(f3)
# 所有的文法都是0型文法
print()
print("产生式的分类：")
print("0型文法：" + " ".join(P) )
print("1型文法：" + " ".join(f1))
print("2型文法：" + " ".join(f2))
print("3型文法：" + " ".join([x[0] for x in f3]))
print()

##### 输出最终的结果 #####
ex = True
if len(f3) == len(P):
    # 是否同时存在左线性和右线性
    has_one = False
    has_two = False
    for _, num in f3:
        if num == 1:
            has_one = True
        elif num == 2:
            has_two = True
    # 不同时存在左线性和右线性
    if not has_one or not has_two:
        print("###该文法是3型文法###")
    else:
        ex = False
else:
    ex = False

# 不是3型文法继续判断
if not ex:
    if len(f2) == len(P):
        print("###该文法是2型文法###")
    elif len(f1) == len(P):
        print("###该文法是1型文法###")
    elif len(f0) == len(P):
        print("###该文法是0型文法###")
    else:
        print("###该文法不是0型文法###")









