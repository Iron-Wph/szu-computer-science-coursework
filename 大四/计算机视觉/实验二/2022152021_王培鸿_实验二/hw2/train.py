import torch
import torchvision.transforms as transforms
import torchvision.datasets as datasets

# 数据增强和归一化
transform_train = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(degrees=10),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
])

transform_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
])

# 加载数据集
train_set = datasets.CIFAR10(root='./data', train=True, transform=transform_train, download=True)
test_set = datasets.CIFAR10(root='./data', train=False, transform=transform_test, download=True)

train_loader = torch.utils.data.DataLoader(train_set, batch_size=128, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=128, shuffle=False)

from model import SimpleNet

# 模型和损失函数和优化器初始化
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleNet().to(device)
total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f'Total trainable parameters: {total_params}')

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)

# 开始训练
epochs = 20
train_losses = []
train_accs = []
test_losses = []
test_accs = []

def train():
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        for i, (input, label) in enumerate(train_loader):
            input, label = input.to(device),label.to(device)
            optimizer.zero_grad()
            output= model(input)
            loss = criterion(output, label)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            # 选取概率最大的类别
            _, predicted = torch.max(output.data, 1)
            total += label.size(0)
            correct += (predicted == label).sum().item()
        
        # 计算准确率
        epoch_loss = running_loss / len(train_loader)
        epoch_acc = 100 * correct / total
        train_losses.append(epoch_loss)
        train_accs.append(epoch_acc)
        # 打印训练信息
        print(f"Epoch [{epoch+1}/{epochs}] | 训练集: Loss: {epoch_loss:.4f}, Acc: {epoch_acc:.2f}%, ", end = "")
        # 每个epoch结束后在测试集上评估
        eval()
        # 最后更新学习概率
        scheduler.step()
            
            
def eval():
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for input, label in test_loader:
            input, label = input.to(device),label.to(device)
            output= model(input)
            loss = criterion(output, label)
            running_loss += loss.item()
            # 选取概率最大的类别
            _, predicted = torch.max(output.data, 1)
            total += label.size(0)
            correct += (predicted == label).sum().item()

    epoch_loss = running_loss / len(test_loader)
    epoch_acc = 100 * correct / total
    test_losses.append(epoch_loss)
    test_accs.append(epoch_acc)
    print(f"测试集: Loss: {epoch_loss:.4f}, Top-1 Acc: {epoch_acc:.2f}%")
    print("-" * 60)

if __name__ == '__main__':
    # 训练模型
    train()
    # 保存模型
    torch.save(model.state_dict(), 'simple_cnn.pth')
    # 绘制训练曲线
    import matplotlib.pyplot as plt
    # 绘制损失曲线
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(range(1, epochs+1), train_losses, label='Training Loss')
    plt.plot(range(1, epochs+1), test_losses, label='Testing Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training and Testing Loss Curves')
    plt.legend()
    plt.grid(True)
    
    # 绘制准确率曲线
    plt.subplot(1, 2, 2)
    plt.plot(range(1, epochs+1), train_accs, label='Training Accuracy')
    plt.plot(range(1, epochs+1), test_accs, label='Testing Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.title('Training and Testing Accuracy Curves')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('training_testing_curves.png')
    plt.show()
    
    # 输出最终测试Top-1准确率
    final_test_acc = test_accs[-1]
    print(f"最终测试集Top-1准确率：{final_test_acc:.2f}%")