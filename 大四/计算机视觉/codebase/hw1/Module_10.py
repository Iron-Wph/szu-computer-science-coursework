 #使用内置模块
import math
import random
from datetime import datetime
# math模块示例
print(f"圆周率: {math.pi}")
print(f"e常数: {math.e}")
print(f"平方根: {math.sqrt(16)}")
print(f"对数: {math.log(100, 10)}")  # 以10为底100的对数
# random模块示例
print(f"随机整数: {random.randint(1, 100)}")
print(f"随机选择: {random.choice(['苹果', '香蕉', '橙子'])}")
# 从0-99中随机选5个不重复的数
print(f"随机采样: {random.sample(range(100), 5)}")  

# 然后使用自定义模块
import mymodule
print(mymodule.greet("孙七"))
print(f"圆面积: {mymodule.calculate_area(5)}")
person = mymodule.Person("吴八", 40)
print(person.introduce())
# 从模块导入特定功能
from mymodule import greet, calculate_area
from math import pi as 圆周率  # 使用别名
print(greet("郑九"))
print(f"更精确的圆周率: {圆周率}")
# 查看模块内容
print(f"math模块的内容: {dir(math)}")
print(f"mymodule模块的内容: {dir(mymodule)}")
 # 使用__name__属性
if __name__ == "__main__":
    print("这个脚本是直接运行的")
else:
    print("这个脚本是作为模块被导入的")