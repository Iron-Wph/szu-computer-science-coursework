# # 字符串创建
# single_quotes = '单引号字符串'
# double_quotes = "双引号字符串"
# triple_quotes = """多行字符串
# 可以换行
# 很方便"""
# # 字符串基本操作
# text = "Python编程"
# print(f"字符串: {text}")
# print(f"长度: {len(text)}")
# print(f"大写: {text.upper()}")
# print(f"小写: {text.lower()}")
# print(f"首字母大写: {text.capitalize()}")
# # 字符串索引和切片
# message = "Hello, World!"
# print(f"第一个字符: {message[0]}")
# print(f"最后一个字符: {message[-1]}")
# print(f"子字符串: {message[0:5]}")  # 切片: 从0到5(不包括5)

# print(f"反向索引: {message[-6:-1]}")  # World
# # 字符串方法
# sentence = " Python 是优秀的编程语言 "
# print(f"原始句子: '{sentence}'")
# print(f"去除空格: '{sentence.strip()}'")
# print(f"替换: '{sentence.replace('Python', 'Java')}'")
# print(f"查找'优秀': {sentence.find('优秀')}")
# print(f"分割: {sentence.split()}")
# print(f"是否以'Py'开头: {sentence.startswith('Py')}")
# print(f"是否以'言'结尾: {sentence.endswith('言')}")
# # 字符串格式化
# name = "Alice"
# age = 25
# # 方法1: f-string (Python 3.6+ 推荐)
# print(f"{name}今年{age}岁")
# # 方法2: format方法
# print("{}今年{}岁".format(name, age))
# # 方法3: %格式化 (较老的方法)
# print("%s今年%d岁" % (name, age))

name = input("请输入您的名字: ")
print(f"格式化后的名字: {name.capitalize()}")