# import torch 

# def func(x, y):
#     return 3* x **2 * y + 2 * y **3

# print("理论偏导值：")
# print(f"df / dx = 12, df  / dy = 18")

# x = torch.tensor(2.0,requires_grad=True)
# y = torch.tensor(1.0,requires_grad=True)

# f = func(x,y)
# f.backward()        # 反向传播求梯度

# print("\n验证结果：")
# print(f"df/dx = {x.grad.item()}, df/dy = {y.grad.item()}")

# # 验证是否与理论值⼀致
# print("\n验证结果：")
# print(f"df/dx 匹配: {abs(x.grad.item() - 12) < 1e-10}")
# print(f"df/dy 匹配: {abs(y.grad.item() - 18) < 1e-10}")

import torch 

def func2(x, y):
    return x **3 * y + 2 * x * y **2 + 5


x = torch.tensor(3.0,requires_grad=True)
y = torch.tensor(2.0,requires_grad=True)

print(f"当x = {x.item()}, y = {y.item()}, 理论偏导值：")
print(f"df / dx = 62, df / dy = 51")

f = func2(x,y)
f.backward()        # 反向传播求梯度

print("\n验证结果：")
print(f"df/dx = {x.grad.item()}, df/dy = {y.grad.item()}")

# 验证是否与理论值⼀致
print("\n验证结果：")
print(f"df/dx 匹配: {abs(x.grad.item() - 62) < 1e-10}")
print(f"df/dy 匹配: {abs(y.grad.item() - 51) < 1e-10}")

#### 更换参数
x = torch.tensor(1.0,requires_grad=True)
y = torch.tensor(4.0,requires_grad=True)

print(f"当x = {x.item()}, y = {y.item()}, 理论偏导值：")
print(f"df / dx = 44, df / dy = 17")

f = func2(x,y)
f.backward()        # 反向传播求梯度

print("\n验证结果：")
print(f"df/dx = {x.grad.item()}, df/dy = {y.grad.item()}")

# 验证是否与理论值⼀致
print("\n验证结果：")
print(f"df/dx 匹配: {abs(x.grad.item() - 44) < 1e-10}")
print(f"df/dy 匹配: {abs(y.grad.item() - 17) < 1e-10}")




