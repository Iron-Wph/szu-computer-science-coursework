# for循环遍历序列
fruits = ["苹果", "香蕉", "橙子", "葡萄"]
print("水果列表:")
for fruit in fruits:
    print(f"- {fruit}")
 # for循环与range()
print("\n数字0到4:")
for i in range(5):  # 0, 1, 2, 3, 4
    print(i)
print("\n数字5到9:")
for i in range(5, 10):  # 5, 6, 7, 8, 9
    print(i)
print("\n偶数0到8:")
for i in range(0, 10, 2):  # 0, 2, 4, 6, 8
    print(i)
 # while循环
print("\nwhile循环计数:")
count = 0
while count < 5:
    print(count)
    count += 1  # 重要：不要忘记更新条件变量，否则会无限循环！
# 循环与else配合
print("\n循环else示例:")
for i in range(3):
    print(i)
else:
    print("循环正常结束")  # 如果循环没有被break中断，会执行else块
    
# 
res = 0
for i in range(1, 101):
    res += i
print("统计1-100的整数之和：", res)