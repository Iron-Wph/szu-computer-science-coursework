import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
# 复⽤SimpleCNN
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=5, padding=2)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=5, padding=2)
        self.fc = nn.Linear(32 * 7 * 7, 10)
    
    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

 # 数据加载
transform = transforms.Compose([
transforms.ToTensor(),
transforms.Normalize((0.1307,), (0.3081,))
])
train_dataset = datasets.MNIST(root='./data', train=True, download=True, 
    transform=transform)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, 
    shuffle=True)
test_dataset = datasets.MNIST(root='./data', train=False, download=True, 
    transform=transform)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=64, 
    shuffle=True)

# 初始化组件与学习率调度器
model = SimpleCNN()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=2, gamma=0.5)  # 每2轮学习率减半
# 训练循环（记录学习率）
epochs = 20
train_losses = []
lrs = []
train_correct = []
test_correct = []
for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    lrs.append(optimizer.param_groups[0]['lr'])  # 记录当前学习率
    for images, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        correct += (predicted == labels).sum().item()
    train_correct.append(correct / len(train_loader.dataset))
    epoch_loss = running_loss / len(train_loader)
    train_losses.append(epoch_loss)
    print(f'Epoch {epoch+1}, Loss: {epoch_loss:.4f}, LR: {lrs[-1]:.6f}', end=' ')
    # 测试集评估
    model.eval()
    correct = 0
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = outputs.max(1)
        correct += (predicted == labels).sum().item()
    test_correct.append(correct / len(test_loader.dataset))
    print(f'Test Accuracy: {correct / len(test_loader.dataset):.4f}')

    scheduler.step()  # 更新学习率

torch.save(model.state_dict(), 'mnist_cnn_weights.pth')

# 绘制损失与学习率曲线
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(range(1, epochs+1), train_losses, 'b-')
plt.title('Training Loss (with LR Scheduler)')
plt.xlabel('Epoch')
plt.subplot(1, 2, 2)
plt.plot(range(1, epochs+1), lrs, 'g-')
plt.title('Learning Rate Schedule')
plt.xlabel('Epoch')
plt.ylabel('LR')
plt.tight_layout()
plt.savefig("lr_scheduler_training.png")

# 绘制训练集与测试集准确率曲线
plt.figure(figsize=(12, 4))
plt.plot(range(1, epochs+1), train_correct, 'b-', label='Train Acc')
plt.plot(range(1, epochs+1), test_correct, 'g-', label='Test Acc')
plt.title('Accuracy (with LR Scheduler)')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.tight_layout()
plt.savefig("lr_scheduler_accuracy.png")
plt.show()
 
