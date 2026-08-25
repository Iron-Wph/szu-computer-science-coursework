# 创建自己的模块

# mymodule.py 内容
def greet(name):
    return f"你好, {name}!"

def calculate_area(radius):
    return 3.14159 * radius ** 2
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def introduce(self):
        return f"我叫{self.name}, 今年{self.age}岁"
