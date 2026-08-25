# import torch 
# import matplotlib.pyplot as plt

# def target_function(x_val):
#     return (x_val - 3)**2 + 5

# # 优化过程
# def optimize(optimize_cls, lr=0.1, momentum=0, steps=50):
#     x = torch.tensor(10.0, requires_grad = True)
#     if optimize_cls.__name__ == 'Adam':
#         # 传入参数和学习率
#         optimizer = optimize_cls([x], lr=lr)
#     else:
#         # 默认是SGD
#         optimizer = optimize_cls([x], lr=lr, momentum=momentum)
    
#     x_history, loss_history = [], []
    
#     # 梯度下降
#     for _ in range(steps):
#         loss = target_function(x)
#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()
#         x_history.append(x.item())
#         loss_history.append(loss.item())
        
#     return x_history, loss_history

# # 测试不同学习率的SGD
# sgd_x1, sgd_loss1 = optimize(torch.optim.SGD, lr=0.05)
# sgd_x2, sgd_loss2 = optimize(torch.optim.SGD, lr=0.2)

# # 测试不同的动量
# momentum_x1, momentum_loss1 = optimize(torch.optim.SGD, lr=0.1, momentum=0.5)
# momentum_x2, momentum_loss2 = optimize(torch.optim.SGD, lr=0.1, momentum=0.95)

# # 测试不同学习率的Adam
# adam_x1, adam_loss1 = optimize(torch.optim.Adam, lr=0.001)
# adam_x2, adam_loss2 = optimize(torch.optim.Adam, lr=0.2)

# # 绘制结果
# plt.figure(figsize=(18, 12))

# # SGD不同学习率对比
# plt.subplot(3, 2, 1)
# plt.plot(sgd_loss1, label='SGD lr=0.05')
# plt.plot(sgd_loss2, label='SGD lr=0.2')
# plt.axhline(y=5, color='r', linestyle='--', label='Optimal')
# plt.title('SGD with Different Learning Rates')
# plt.xlabel('Steps')
# plt.ylabel('Loss')
# plt.legend()

# # SGD不同动量对比
# plt.subplot(3, 2, 3)
# plt.plot(momentum_loss1, label='SGD momentum=0.5')
# plt.plot(momentum_loss2, label='SGD momentum=0.95')
# plt.axhline(y=5, color='r', linestyle='--', label='Optimal')
# plt.title('Momentum SGD with Different Momentums')
# plt.xlabel('Steps')
# plt.ylabel('Loss')
# plt.legend()

# # Adam不同学习率对比
# plt.subplot(3, 2, 5)
# plt.plot(adam_loss1, label='Adam lr=0.001')
# plt.plot(adam_loss2, label='Adam lr=0.2')
# plt.axhline(y=5, color='r', linestyle='--', label='Optimal')
# plt.title('Adam with Different Learning Rates')
# plt.xlabel('Steps')
# plt.ylabel('Loss')
# plt.legend()

# # x值收敛过程对⽐
# plt.subplot(3, 2, 2)
# plt.plot(sgd_x1, label='SGD lr=0.05')
# plt.plot(sgd_x2, label='SGD lr=0.2')
# plt.axhline(y=3, color='r', linestyle='--', label='Optimal x')
# plt.title('x Convergence for SGD')
# plt.xlabel('Steps')
# plt.ylabel('x Value')
# plt.legend()
# plt.subplot(3, 2, 4)
# plt.plot(momentum_x1, label='Momentum=0.5')
# plt.plot(momentum_x2, label='Momentum=0.95')
# plt.axhline(y=3, color='r', linestyle='--', label='Optimal x')
# plt.title('x Convergence for Momentum')
# plt.xlabel('Steps')
# plt.ylabel('x Value')
# plt.legend()
# plt.subplot(3, 2, 6)
# plt.plot(adam_x1, label='Adam lr=0.001')
# plt.plot(adam_x2, label='Adam lr=0.2')
# plt.axhline(y=3, color='r', linestyle='--', label='Optimal x')
# plt.title('x Convergence for Adam')
# plt.xlabel('Steps')
# plt.ylabel('x Value')
# plt.legend()

# plt.tight_layout()
# plt.savefig('optimizer_comparison.png')
# plt.show()
# print("总结：")
# print("1. 学习率过⼩：收敛速度慢，需要更多迭代才能达到最优")
# print("2. 学习率过⼤：可能导致震荡，甚⾄发散，⽆法收敛到最优值")
# print("3. 动量过⼩：收敛速度较慢，容易陷⼊局部最优")
# print("4. 动量过⼤：可能在最优值附近震荡，收敛不稳定")


import torch 
import matplotlib.pyplot as plt

def target_function(x, y):
    return (x - 2)**2 + 2 * (y + 1)**2 + 3

# 优化过程
def optimize(optimize_cls, lr=0.1, momentum=0, alpha = 0.99, steps=50):
    x = torch.tensor(5.0, requires_grad = True)
    y = torch.tensor(2.0, requires_grad = True)
    
    if optimize_cls.__name__ == 'Adam':
        # 传入参数和学习率
        # 默认固定β1=0.9, β2=0.999
        optimizer = optimize_cls([x, y], lr=lr)
    elif optimize_cls.__name__ == 'RMSprop':
        # 默认固定衰减率α=0.99
        optimizer = optimize_cls([x, y], lr=lr, alpha=alpha)
    else:
        # 默认是SGD
        optimizer = optimize_cls([x, y], lr=lr, momentum=momentum)
    
    x_history, y_history, loss_history = [], [], []
    
    # 梯度下降
    for _ in range(steps):
        loss = target_function(x, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        x_history.append(x.item())
        y_history.append(y.item())
        loss_history.append(loss.item())
        
    return x_history, y_history, loss_history

# 测试不同学习率的SGD
sgd_x1, sgd_y1, sgd_loss1 = optimize(torch.optim.SGD, lr=0.05)
sgd_x2, sgd_y2, sgd_loss2 = optimize(torch.optim.SGD, lr=0.3)

# 测试不同的动量
momentum_x1, momentum_y1, momentum_loss1 = optimize(torch.optim.SGD, lr=0.1, momentum=0.6)
momentum_x2, momentum_y2, momentum_loss2 = optimize(torch.optim.SGD, lr=0.1, momentum=0.9)

# 测试不同学习率的Adam
adam_x1, adam_y1, adam_loss1 = optimize(torch.optim.Adam, lr=0.01)
adam_x2, adam_y2, adam_loss2 = optimize(torch.optim.Adam, lr=0.05)

# 测试不同衰减率的RMSprop
rms_x1, rms_y1, rms_loss1 = optimize(torch.optim.RMSprop, lr=0.05, alpha=0.8)
rms_x2, rms_y2, rms_loss2 = optimize(torch.optim.RMSprop, lr=0.05, alpha=0.99)

# 绘制结果
plt.figure(figsize=(24, 18))

# SGD不同学习率对比
plt.subplot(4, 3, 1)
plt.plot(sgd_loss1, label='SGD lr=0.05')
plt.plot(sgd_loss2, label='SGD lr=0.2')
plt.axhline(y=3, color='r', linestyle='--', label='Optimal')
plt.title('SGD with Different Learning Rates')
plt.xlabel('Steps')
plt.ylabel('Loss')
plt.legend()

# SGD不同动量对比
plt.subplot(4, 3, 4)
plt.plot(momentum_loss1, label='SGD momentum=0.5')
plt.plot(momentum_loss2, label='SGD momentum=0.95')
plt.axhline(y=3, color='r', linestyle='--', label='Optimal')
plt.title('Momentum SGD with Different Momentums')
plt.xlabel('Steps')
plt.ylabel('Loss')
plt.legend()

# Adam不同学习率对比
plt.subplot(4, 3, 7)
plt.plot(adam_loss1, label='Adam lr=0.001')
plt.plot(adam_loss2, label='Adam lr=0.2')
plt.axhline(y=3, color='r', linestyle='--', label='Optimal')
plt.title('Adam with Different Learning Rates')
plt.xlabel('Steps')
plt.ylabel('Loss')
plt.legend()

# RMSprop不同衰减率对比
plt.subplot(4, 3, 10)
plt.plot(rms_loss1, label='RMSprop alpha=0.8')
plt.plot(rms_loss2, label='RMSprop alpha=0.99')
plt.axhline(y=3, color='r', linestyle='--', label='Optimal')
plt.title('RMSprop with Different Decay Rates')
plt.xlabel('Steps')
plt.ylabel('Loss')
plt.legend()

# x值收敛过程对⽐
plt.subplot(4, 3, 2)
plt.plot(sgd_x1, label='SGD lr=0.05')
plt.plot(sgd_x2, label='SGD lr=0.2')
plt.axhline(y=2, color='r', linestyle='--', label='Optimal x')
plt.title('x Convergence for SGD')
plt.xlabel('Steps')
plt.ylabel('x Value')
plt.legend()
plt.subplot(4, 3, 5)
plt.plot(momentum_x1, label='Momentum=0.5')
plt.plot(momentum_x2, label='Momentum=0.95')
plt.axhline(y=2, color='r', linestyle='--', label='Optimal x')
plt.title('x Convergence for Momentum')
plt.xlabel('Steps')
plt.ylabel('x Value')
plt.legend()
plt.subplot(4, 3, 8)
plt.plot(adam_x1, label='Adam lr=0.001')
plt.plot(adam_x2, label='Adam lr=0.2')
plt.axhline(y=2, color='r', linestyle='--', label='Optimal x')
plt.title('x Convergence for Adam')
plt.xlabel('Steps')
plt.ylabel('x Value')
plt.legend()
plt.subplot(4, 3, 11)
plt.plot(rms_x1, label='RMSprop alpha=0.8')
plt.plot(rms_x2, label='RMSprop alpha=0.99')
plt.axhline(y=2, color='r', linestyle='--', label='Optimal x')
plt.title('x Convergence for RMSprop')
plt.xlabel('Steps')
plt.ylabel('x Value')
plt.legend()

# y值收敛过程对⽐
plt.subplot(4, 3, 3)
plt.plot(sgd_y1, label='SGD lr=0.05')
plt.plot(sgd_y2, label='SGD lr=0.2')
plt.axhline(y=-1, color='r', linestyle='--', label='Optimal y')
plt.title('y Convergence for SGD')
plt.xlabel('Steps')
plt.ylabel('y Value')
plt.legend()
plt.subplot(4, 3, 6)
plt.plot(momentum_y1, label='Momentum=0.5')
plt.plot(momentum_y2, label='Momentum=0.95')
plt.axhline(y=-1, color='r', linestyle='--', label='Optimal y')
plt.title('y Convergence for Momentum')
plt.xlabel('Steps')
plt.ylabel('y Value')
plt.legend()
plt.subplot(4, 3, 9)
plt.plot(adam_y1, label='Adam lr=0.001')
plt.plot(adam_y2, label='Adam lr=0.2')
plt.axhline(y=-1, color='r', linestyle='--', label='Optimal y')
plt.title('y Convergence for Adam')
plt.xlabel('Steps')
plt.ylabel('y Value')
plt.legend()
plt.subplot(4, 3, 12)
plt.plot(rms_y1, label='RMSprop alpha=0.8')
plt.plot(rms_y2, label='RMSprop alpha=0.99')
plt.axhline(y=-1, color='r', linestyle='--', label='Optimal y')
plt.title('y Convergence for RMSprop')
plt.xlabel('Steps')
plt.ylabel('y Value')
plt.legend()

plt.tight_layout()          # 自动调间距，防止子图重叠
plt.savefig('optimizer_comparison2.png')
plt.show()
