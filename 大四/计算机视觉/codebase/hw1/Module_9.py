# 定义一个简单的类
class Dog:
    # 类属性（所有狗共享）
    species = "Canis familiaris"
    # 初始化方法（构造方法）
    def __init__(self, name, age):
        # 实例属性（每个对象独有）
        self.name = name
        self.age = age
    # 实例方法
    def bark(self):
        return f"{self.name} 说: 汪汪!"
# 创建对象（类的实例）
my_dog = Dog("Buddy", 3)
your_dog = Dog("Lucy", 5)
print(my_dog.name)    # 输出: Buddy
print(your_dog.age)   # 输出: 5
print(my_dog.bark())  # 输出: Buddy 说: 汪汪!

class BankAccount:
    def __init__(self, account_holder, initial_balance=0):
        self.account_holder = account_holder
        # 私有属性（双下划线开头）[2,4](@ref)
        self.__balance = initial_balance  
    # 公有方法用于访问私有属性
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"存款成功: {amount}元")
        else:
            print("存款金额必须大于0")
    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"取款成功: {amount}元")
        else:
            print("取款金额无效或余额不足")
    def get_balance(self):
        return self.__balance
    def get_account_info(self):
        return f"账户持有人: {self.account_holder} \
            , 余额: {self.__balance}元"
# 使用银行账户类
account = BankAccount("张三", 1000)
account.deposit(500)
account.withdraw(200)
print(account.get_account_info())
# 尝试直接访问私有属性（会失败）
# print(account.__balance)  # 报错: AttributeError
 