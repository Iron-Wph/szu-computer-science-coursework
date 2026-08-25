# # 字典创建
# person = {
#     "name": "李四",
#     "age": 28,
#     "city": "北京",
#     "is_student": False
# }
# print(f"个人信息: {person}")
# # 访问字典值
# print(f"姓名: {person['name']}")
# print(f"年龄: {person.get('age')}")
# print(f"职业: {person.get('job', '未知')}")  # 提供默认值
# # 修改字典
# person["age"] = 29  # 更新值
# person["job"] = "工程师"  # 添加新键值对
# print(f"更新后: {person}")
# # 字典方法
# print(f"所有键: {person.keys()}")
# print(f"所有值: {person.values()}")
# print(f"所有键值对: {person.items()}")
# # 遍历字典
# print("\n遍历字典:")
# for key in person:
#     print(f"{key}: {person[key]}")
# print("\n遍历键值对:")
# for key, value in person.items():
#     print(f"{key}: {value}")
# # 字典推导式
# words = ["apple", "banana", "cherry"]
# word_lengths = {word: len(word) for word in words}
# print(f"单词长度映射: {word_lengths}")
# # 复杂字典：嵌套数据结构
# students = {
#     "001": {
#         "name": "王五",
#         "scores": {"数学": 90, "英语": 85, "物理": 88}
#     },
#     "002": {
#         "name": "赵六",
#         "scores": {"数学": 78, "英语": 92, "物理": 85}
#     }
# }
# print(f"学生数据: {students}")
# print(f"001号学生的数学成绩: {students['001']['scores']['数学']}")

def display_menu():
    """显示操作菜单"""
    print("\n===== 电话簿 =====")
    print("1. 添加联系人")
    print("2. 查找联系人")
    print("3. 删除联系人")
    print("4. 显示所有联系人")
    print("5. 退出")
    print("==================")

def add_contact(phone_book):
    """添加联系人到电话簿"""
    name = input("请输入联系人姓名: ").strip()
    if name in phone_book:
        print(f"警告: 联系人 '{name}' 已存在!")
        update = input("是否更新电话号码? (y/n): ").lower()
        if update != 'y':
            return
    
    phone = input("请输入电话号码: ").strip()
    phone_book[name] = phone
    print(f"联系人 '{name}' 已添加/更新成功!")

def find_contact(phone_book):
    """查找联系人"""
    name = input("请输入要查找的联系人姓名: ").strip()
    if name in phone_book:
        print(f"{name}: {phone_book[name]}")
    else:
        print(f"未找到联系人 '{name}'")

def delete_contact(phone_book):
    """删除联系人"""
    name = input("请输入要删除的联系人姓名: ").strip()
    if name in phone_book:
        confirm = input(f"确定要删除 '{name}' 吗? (y/n): ").lower()
        if confirm == 'y':
            del phone_book[name]
            print(f"联系人 '{name}' 已删除")
    else:
        print(f"未找到联系人 '{name}'")

def display_all(phone_book):
    """显示所有联系人"""
    if not phone_book:
        print("电话簿为空")
        return
    
    print("\n所有联系人:")
    for name, phone in sorted(phone_book.items()):
        print(f"{name}: {phone}")

def main():
    """主函数，控制程序流程"""
    phone_book = {}  # 用字典存储联系人，键为姓名，值为电话号码
    
    while True:
        display_menu()
        choice = input("请选择操作 (1-5): ").strip()
        
        if choice == '1':
            add_contact(phone_book)
        elif choice == '2':
            find_contact(phone_book)
        elif choice == '3':
            delete_contact(phone_book)
        elif choice == '4':
            display_all(phone_book)
        elif choice == '5':
            print("谢谢使用，再见!")
            break
        else:
            print("无效的选择，请重新输入 (1-5)")

if __name__ == "__main__":
    main()
    