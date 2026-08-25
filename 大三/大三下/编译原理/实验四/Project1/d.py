import os
import sys

# 请在此输入您的代码
t = int(input())
zhi = [8 ,4 ,2]
for i in range(t):
    a, b = input().split()
    b = int(b)
    # print(f"a: {a}, b: {b}")
    count = 0
    if a.isdigit():
        for k in range(len(zhi)):
            if int(a, zhi[k]) <= b:
                count += 1
        if count != 1:
            print("-1")
        else:
            print(int(a, zhi[-1]))
    else:
        if int(a, 16) <= b:
                count += 1
        if count != 1:
            print("-1")
        else:
            print(int(a, 16))
