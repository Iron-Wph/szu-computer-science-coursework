import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from torchvision import datasets, transforms
import torch.optim as optim

# 类别名称
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# 带BN的CNN模型
class CNNWithBatchNorm(nn.Module):
    def __init__(self):
        super(CNNWithBatchNorm, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=5, padding=2)
        self.bn1 = nn.BatchNorm2d(16)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=5, padding=2)
        self.bn2 = nn.BatchNorm2d(32)
        self.fc = nn.Linear(32 * 7 * 7, 10)
        
    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        self.feature_conv1 = x
        x = self.pool(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)
        self.feature_conv2 = x
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

# 数据转换
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.2860,), (0.3530,))
])

# 加载数据集 - 确保训练集和测试集一致
test_dataset = datasets.FashionMNIST(
    root='./data', train=False, download=True, transform=transform
)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=64, shuffle=False)

train_dataset = datasets.FashionMNIST(
    root='./data', train=True, download=True, transform=transform
)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)

# 模型训练与保存
model = CNNWithBatchNorm()
'''
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=2, gamma=0.5)

epochs = 5
for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    
    epoch_loss = running_loss / len(train_loader)
    print(f'Epoch {epoch+1}, Loss: {epoch_loss:.4f}, LR: {optimizer.param_groups[0]["lr"]:.6f}')
    scheduler.step()

torch.save(model.state_dict(), 'fashion_cnn_bn_weights.pth')
'''
model.load_state_dict(torch.load('fashion_cnn_bn_weights.pth'))

# 收集错误案例 - 使用独立的图像对象
model.eval()
misclassified_images = []
misclassified_trues = []
misclassified_preds = []

with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = outputs.max(1)
        errors = labels != predicted
        if errors.any():
            misclassified_images.extend(images[errors])
            misclassified_trues.extend(labels[errors])
            misclassified_preds.extend(predicted[errors])
            if len(misclassified_images) >= 20:
                break

# 保存错误案例图像 - 使用独立的fig对象并确保关闭
# 关键修复1：创建独立的图像对象
fig_misclassified = plt.figure(figsize=(15, 8))
for i in range(20):
    ax = fig_misclassified.add_subplot(4, 5, i+1)
    ax.imshow(misclassified_images[i][0].numpy(), cmap='gray')
    true_name = class_names[misclassified_trues[i].item()]
    pred_name = class_names[misclassified_preds[i].item()]
    ax.set_title(f"True: {true_name}\nPred: {pred_name}", color='red')
    ax.axis('off')

fig_misclassified.tight_layout()
fig_misclassified.savefig("fashion_mnist_misclassified.png")
# 关键修复2：明确关闭当前图像对象，避免内容残留
plt.close(fig_misclassified)

# 特征可视化部分
samples = []
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

for idx in [0, 10]:
    img_tensor = torch.Tensor(misclassified_images[idx].numpy())
    # 反归一化
    inv_transform = transforms.Normalize(
        (-0.2860/0.3530,), (1/0.3530,)
    )
    img_original = inv_transform(img_tensor)
    img_original = torch.clamp(img_original, 0, 1)
    samples.append({
        'original': img_original, 
        'tensor': img_tensor.unsqueeze(0).to(device), 
        'label': misclassified_trues[idx],
        'pred': misclassified_preds[idx]
    })

def visualize_feature_map(feature_tensor, num_channels=3):
    feature = feature_tensor.squeeze(0).cpu().detach()
    if feature.shape[0] > num_channels:
        feature = feature[:num_channels, :, :]
    feature_min = feature.min()
    feature_max = feature.max()
    feature_norm = (feature - feature_min) / (feature_max - feature_min + 1e-8)
    if num_channels == 1:
        feature_vis = feature_norm.permute(1, 2, 0).repeat(1, 1, 3)
    else:
        feature_vis = feature_norm.permute(1, 2, 0)
    return feature_vis

# 关键修复3：创建全新的图像对象用于特征可视化
fig_features = plt.figure(figsize=(20, 10))
fig_features.suptitle("Feature visualization")

# 处理第一个样本
sample1 = samples[0]
with torch.no_grad():
    model(sample1['tensor'])

ax1 = fig_features.add_subplot(2, 3, 1)
ax1.imshow(sample1['original'].squeeze().numpy(), cmap='gray')
ax1.set_title(f'Sample 1\nOriginal Image\nLabel: {class_names[sample1["label"]]}')
ax1.axis('off')

ax2 = fig_features.add_subplot(2, 3, 2)
conv1_feat = visualize_feature_map(model.feature_conv1)
ax2.imshow(conv1_feat)
ax2.set_title(f'Conv1 Output\nShape: {model.feature_conv1.shape[2:]}\npred: {class_names[sample1["pred"]]}')
ax2.axis('off')

ax3 = fig_features.add_subplot(2, 3, 3)
conv2_feat = visualize_feature_map(model.feature_conv2)
ax3.imshow(conv2_feat)
ax3.set_title(f'Conv2 Output\nShape: {model.feature_conv2.shape[2:]}\npred: {class_names[sample1["pred"]]}')
ax3.axis('off')

# 处理第二个样本
sample2 = samples[1]
with torch.no_grad():
    model(sample2['tensor'])

ax4 = fig_features.add_subplot(2, 3, 4)  # 注意索引是5而不是1，确保在第二行
ax4.imshow(sample2['original'].squeeze().numpy(), cmap='gray')  # 修复：使用sample2
ax4.set_title(f'Sample 2\nOriginal Image\nLabel: {class_names[sample2["label"]]}')  # 修复：使用sample2
ax4.axis('off')

ax5 = fig_features.add_subplot(2, 3, 5)
conv1_feat = visualize_feature_map(model.feature_conv1)
ax5.imshow(conv1_feat)
ax5.set_title(f'Conv1 Output\nShape: {model.feature_conv1.shape[2:]}\npred: {class_names[sample2["pred"]]}')
ax5.axis('off')

ax6 = fig_features.add_subplot(2, 3, 6)
conv2_feat = visualize_feature_map(model.feature_conv2)
ax6.imshow(conv2_feat)
ax6.set_title(f'Conv2 Output\nShape: {model.feature_conv2.shape[2:]}\npred: {class_names[sample2["pred"]]}')
ax6.axis('off')

# 保存并关闭特征可视化图像
fig_features.tight_layout()
fig_features.savefig('feature_visualization_updated.png')
plt.close(fig_features)  # 关键修复4：明确关闭特征可视化图像
