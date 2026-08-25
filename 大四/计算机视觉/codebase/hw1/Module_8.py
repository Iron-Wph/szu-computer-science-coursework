# # 基本函数定义
# def greet(name):
#     """简单的问候函数"""
#     return f"你好, {name}!"
#  # 调用函数
# message = greet("王小明")
# print(message)
# # 带默认参数的函数
# def introduce(name, age, city="北京"):
#     """自我介绍函数"""
#     return f"我叫{name}，今年{age}岁，来自{city}。"
# print(introduce("张三", 25))
# print(introduce("李四", 30, "上海"))
# # 可变参数
# def calculate_average(*numbers):
#     """计算任意数量数字的平均值"""
#     if not numbers:
#         return 0
#     return sum(numbers) / len(numbers)
# print(f"平均值1: {calculate_average(1, 2, 3, 4, 5)}")
# print(f"平均值2: {calculate_average(10, 20, 30)}")
# # 关键字参数
# def create_person(**attributes):
#     """通过关键字参数创建人物信息"""
#     person = {}
#     for key, value in attributes.items():
#         person[key] = value
#     return person
# person_info = create_person(name="赵五", age=35, occupation="医生")
# print(f"创建的人物: {person_info}")
# # 返回多个值
# def calculate_statistics(numbers):
#     """计算数字列表的统计信息"""
#     total = sum(numbers)
#     count = len(numbers)
#     average = total / count if count > 0 else 0
#     maximum = max(numbers) if numbers else 0
#     minimum = min(numbers) if numbers else 0
#     return total, average, maximum, minimum
# stats = calculate_statistics([10, 20, 30, 40, 50])
# total, average, maximum, minimum = stats
# print(f"总和: {total}, 平均: {average}, 最大: {maximum}, 最小: {minimum}")
# # 递归函数示例
# def factorial(n):
#     """计算阶乘的递归函数"""
#     if n == 0 or n == 1:
#         return 1
#     else:
#         return n * factorial(n - 1)
# print(f"5的阶乘: {factorial(5)}")
# # lambda函数（匿名函数）
# square = lambda x: x ** 2
# print(f"5的平方: {square(5)}")
# # 在列表排序中使用lambda
# people = [
#     {"name": "张三", "age": 25},
#     {"name": "李四", "age": 20},
#     {"name": "王五", "age": 30}
# ]
# # 按年龄排序
# sorted_people = sorted(people, key=lambda x: x["age"])
# print(f"按年龄排序: {sorted_people}")

import random

def validate_parameters(min_num, max_num, max_attempts):
    """验证游戏参数是否有效"""
    if not isinstance(min_num, int) or not isinstance(max_num, int) \
        or not isinstance(max_attempts, int):
        raise TypeError("所有参数必须是整数")
    if min_num >= max_num:
        raise ValueError("最小值必须小于最大值")
    if max_attempts <= 0:
        raise ValueError("最大尝试次数必须是正数")
    
    return True

def play_guess_number(min_num=1, max_num=100, max_attempts=10):
    """
    猜数字游戏主函数
    参数:
        min_num: 数字范围最小值
        max_num: 数字范围最大值
        max_attempts: 最大尝试次数
    """
    try:
        validate_parameters(min_num, max_num, max_attempts)
    except (TypeError, ValueError) as e:
        print(f"游戏参数错误: {e}")
        return
    
    # 生成目标数字
    target_number = random.randint(min_num, max_num)
    attempts = 0
    print(f"欢迎来到猜数字游戏!")
    print(f"我已经想好了一个介于 {min_num} 和 {max_num} 之间的数字")
    print(f"你有 {max_attempts} 次机会猜出它\n")

    while attempts < max_attempts:
        # 计算剩余次数
        remaining = max_attempts - attempts
        # 获取并验证用户输入
        try:
            guess = input(f"请输入你的猜测 ({remaining} 次机会 remaining): ")
            guess = int(guess)
            # 检查猜测是否在有效范围内
            if guess < min_num or guess > max_num:
                print(f"请输入 {min_num} 到 {max_num} 之间的数字!")
                continue
        except ValueError:
            print("请输入有效的整数!")
            continue
        # 增加尝试次数
        attempts += 1
        # 检查猜测结果
        if guess < target_number:
            print("太小了! 再试一次\n")
        elif guess > target_number:
            print("太大了! 再试一次\n")
        else:
            print(f"\n恭喜你! 你猜对了! 答案就是 {target_number}")
            print(f"你用了 {attempts} 次猜出了正确答案")
            return
    # 如果用完所有机会仍未猜对
    print(f"\n游戏结束! 你已经用完了所有 {max_attempts} 次机会")
    print(f"正确答案是: {target_number}")

if __name__ == "__main__":
    play_guess_number(min_num=1, max_num=50, max_attempts=8)
    