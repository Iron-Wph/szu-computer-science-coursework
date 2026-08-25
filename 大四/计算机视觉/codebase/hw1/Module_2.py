# break语句 - 完全退出循环
print("break示例: 遇到3时退出循环")
for i in range(1, 6):
    if i == 3:
        print("遇到3，退出循环")
        break
    print(f"当前数字: {i}")
 # continue语句 - 跳过当前迭代
print("\ncontinue示例: 跳过奇数")
for i in range(1, 6):
    if i % 2 != 0:  # 如果是奇数
        continue     # 跳过后续代码，继续下一次循环
    print(f"偶数: {i}")
 # pass语句 - 占位符，不执行任何操作
print("\npass示例: 占位使用")
for i in range(3):
    if i == 1:
        pass  # 什么都不做，只是占位
    else:
        print(f"数字: {i}")
 # 综合示例: 查找质数
print("\n查找10以内的质数:")
for num in range(2, 10):
    for i in range(2, num):
        if num % i == 0:  # 如果能被整除，不是质数
            break
    else:
        # for循环的else块: 如果循环正常结束(没有被break)，执行这里
        print(f"{num} 是质数")