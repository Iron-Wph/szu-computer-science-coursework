# import torch
# import torch.nn as nn
# import torch.optim as optim
# import matplotlib.pyplot as plt 
# import numpy as np

# class customNN(nn.Module):
#     def __init__(self):
#         super(customNN, self).__init__()
#         self.fc1 = nn.Linear(2, 16)
#         self.relu = nn.ReLU()
#         self.fc2 = nn.Linear(16, 1)
        
#     def forward(self, x):
#         x = self.fc1(x)
#         x = self.relu(x)
#         x = self.fc2(x)
#         return x

# # 构造随机数据
# np.random.seed(42)
# torch.manual_seed(42)
# num_samples = 1000
# X = torch.tensor(np.random.rand(num_samples, 2), dtype=torch.float32)
# y = torch.tensor([[X[i, 0] + X[i, 1]] for i in range(num_samples)], dtype=torch.float32)

# model =customNN()
# critertion = nn.MSELoss()
# optimizer = optim.Adam(model.parameters(), lr=0.01)

# epochs = 1000
# loss_history = []

# for epoch in range(epochs):
#     outputs = model(X)
#     loss = critertion(outputs, y)
#     optimizer.zero_grad()
#     loss.backward()
#     optimizer.step()
#     loss_history.append(loss.item())
#     if (epoch+1) % 100 == 0:
#         print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')


# # 绘制损失曲线
# plt.figure(figsize=(10,4))
# plt.plot(range(1, epochs + 1 ), loss_history)
# plt.title("Loss Reduction Curve")
# plt.xlabel('Epoch')
# plt.ylabel('Loss')
# plt.grid(True)
# plt.savefig('loss_curve.png')
# plt.show()

# # 模型测试
# test_inputs = torch.tensor([[1.0, 2.0], [3.0, 4.0], [-1.0, 5.0]], 
# dtype=torch.float32)

# with torch.no_grad():
#     predictions = model(test_inputs)

# print("\n测试结果：")
# for i in range(len(test_inputs)):
#     actual = test_inputs[i,0] + test_inputs[i,1]
#     print(f"输⼀: {test_inputs[i].numpy()}, 预测值: {predictions[i].item():.4f}, \
#         实际值: {actual.item()}")


import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt 
import numpy as np

class customNN(nn.Module):
    def __init__(self):
        super(customNN, self).__init__()
        self.fc1 = nn.Linear(3, 32)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(32, 16)
        self.fc3 = nn.Linear(16, 1)
        
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        return x

# 构造随机数据
np.random.seed(42)
torch.manual_seed(42)
num_samples = 1000

X = torch.tensor(np.random.rand(num_samples, 3), dtype=torch.float32)
y = torch.tensor([[2 * X[i, 0] + 3 * X[i, 1] - X[i, 2] + 0.5] for i in range(num_samples)], dtype=torch.float32)

model =customNN()
critertion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.005)

epochs = 200
loss_history = []

for epoch in range(epochs):
    outputs = model(X)
    loss = critertion(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    loss_history.append(loss.item())
    if (epoch+1) % 20 == 0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')


# 绘制损失曲线
plt.figure(figsize=(10,4))
plt.plot(range(1, epochs + 1 ), loss_history)
plt.title("Loss Reduction Curve")
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.grid(True)
plt.savefig('loss_curve2.png')
plt.show()

# 模型测试
test_inputs = torch.tensor([[1.0, 2.0, 3.0], [3.0, 4.0, 5.0], [-1.0, 5.0, 6.0]], 
                            dtype=torch.float32)

with torch.no_grad():
    predictions = model(test_inputs)

print("\n测试结果：")
for i in range(len(test_inputs)):
    actual = 2 * test_inputs[i, 0] + 3 * test_inputs[i, 1] - test_inputs[i, 2] + 0.5
    print(f"输⼀: {test_inputs[i].numpy()}, 预测值: {predictions[i].item():.4f}, \
        实际值: {actual.item()}")
