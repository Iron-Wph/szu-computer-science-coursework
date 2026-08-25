# # 元组创建
# coordinates = (10, 20)
# colors = ("红色", "绿色", "蓝色")
# single_element = (42,)  # 注意逗号，单个元素时必须加
# print(f"坐标: {coordinates}")
# print(f"颜色: {colors}")
# # 元组操作
# print(f"第一个颜色: {colors[0]}")
# print(f"最后两个颜色: {colors[-2:]}")
# print(f"元组长度: {len(colors)}")
# # 元组解包
# x, y = coordinates
# print(f"X坐标: {x}, Y坐标: {y}")
# first, second, third = colors
# print(f"第一颜色: {first}, 第二颜色: {second}")
# # 元组与列表转换
# fruits_list = ["苹果", "香蕉", "橙子"]
# fruits_tuple = tuple(fruits_list)
# print(f"列表转元组: {fruits_tuple}")
# back_to_list = list(fruits_tuple)
# print(f"元组转列表: {back_to_list}")
# # 使用场景：返回多个值
# def get_user_info():
#     name = "张三"
#     age = 30
#     email = "zhangsan@email.com"
#     return name, age, email  # 实际上返回一个元组
# user_info = get_user_info()
# print(f"用户信息: {user_info}")
# # 解包返回值
# name, age, email = get_user_info()
# print(f"姓名: {name}, 年龄: {age}, 邮箱: {email}")

import time

# 1. 数据安全演示：元组不可变，列表可变
def data_safety_demo():
    print("=== 数据安全演示 ===")
    # 元组不可变，保护数据不被意外修改
    person_tuple = ("Alice", 30, "工程师")
    try:
        person_tuple[1] = 31  # 尝试修改元组
    except TypeError as e:
        print(f"元组修改尝试: {e}")  # 会抛出错误，保护数据
    
    # 列表可变，数据可能被意外修改
    person_list = ["Alice", 30, "工程师"]
    person_list[1] = 31  # 可以修改
    print(f"列表修改结果: {person_list}")  # 数据已被改变
    print()

# 2. 性能演示：元组创建和访问速度更快
def performance_demo():
    print("=== 性能演示 ===")
    # 测试创建速度
    start = time.time()
    for _ in range(1000000):
        t = (1, 2, 3, 4, 5)  # 创建元组
    tuple_create_time = time.time() - start
    
    start = time.time()
    for _ in range(1000000):
        l = [1, 2, 3, 4, 5]  # 创建列表
    list_create_time = time.time() - start
    
    print(f"元组创建时间: {tuple_create_time:.6f}秒")
    print(f"列表创建时间: {list_create_time:.6f}秒")
    print(f"元组快 {list_create_time/tuple_create_time:.2f} 倍")
    
    # 测试访问速度
    t = tuple(range(1000))
    l = list(range(1000))
    
    start = time.time()
    for _ in range(1000000):
        x = t[500]  # 访问元组元素
    tuple_access_time = time.time() - start
    
    start = time.time()
    for _ in range(1000000):
        x = l[500]  # 访问列表元素
    list_access_time = time.time() - start
    
    print(f"\n元组访问时间: {tuple_access_time:.6f}秒")
    print(f"列表访问时间: {list_access_time:.6f}秒")
    print()

# 3. 哈希性演示：元组可作为字典键，列表不行
def hashability_demo():
    print("=== 哈希性演示 ===")
    # 元组可以作为字典键
    tuple_dict = {("Alice", "北京"): 13812345678}
    print(f"元组作为字典键: {tuple_dict}")
    
    # 列表不能作为字典键
    try:
        list_dict = {["Alice", "北京"]: 13812345678}
    except TypeError as e:
        print(f"列表作为字典键: {e}")

if __name__ == "__main__":
    data_safety_demo()
    performance_demo()
    hashability_demo()
