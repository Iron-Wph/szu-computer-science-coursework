# # 列表创建和基本操作
# fruits = ["苹果", "香蕉", "橙子", "葡萄", "芒果"]
# print(f"水果列表: {fruits}")
# print(f"第一个水果: {fruits[0]}")
# print(f"最后一个水果: {fruits[-1]}")
# print(f"前两个水果: {fruits[0:2]}")
# print(f"列表长度: {len(fruits)}")
#  # 修改列表
# fruits[1] = "蓝莓"  # 修改第二个元素
# print(f"修改后: {fruits}")
# fruits.append("草莓")  # 添加元素到末尾
# print(f"添加后: {fruits}")
# fruits.insert(2, "菠萝")  # 插入到指定位置
# print(f"插入后: {fruits}")
# removed_fruit = fruits.pop()  # 移除并返回最后一个元素
# print(f"移除: {removed_fruit}, 剩余: {fruits}")
# fruits.remove("橙子")  # 移除指定元素
# print(f"移除橙子后: {fruits}")
# # 列表操作
# numbers = [1, 2, 3]
# more_numbers = [4, 5, 6]
# combined = numbers + more_numbers  # 列表拼接
# print(f"拼接后: {combined}")
# repeated = numbers * 3  # 列表重复
# print(f"重复三次: {repeated}")
# # 列表方法
# print(f"蓝莓的位置: {fruits.index('蓝莓')}")
# print(f"包含苹果吗? {'苹果' in fruits}")
# fruits.sort()  # 排序
# print(f"排序后: {fruits}")
# fruits.reverse()  # 反转
# print(f"反转后: {fruits}")
# # 列表推导式 (强大功能!)
# squares = [x**2 for x in range(10)]
# print(f"平方数列表: {squares}")
# even_squares = [x**2 for x in range(10) if x % 2 == 0]
# print(f"偶数的平方: {even_squares}")

nums = [i for i in range(0, 10)]
news = [i*2 for i in nums if i % 2 == 0]
print("原始列表：", nums)
print("新列表：", news)
