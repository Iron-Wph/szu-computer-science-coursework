import torch
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from model import SimpleNet

# 加载模型权重
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleNet().to(device)
model.load_state_dict(torch.load('simple_cnn.pth', map_location=device))
model.eval()  # 评估模式，禁用Dropout和BN更新

# -------------------------- 2. 读取CIFAR-10数据集（保持原逻辑，确保数据预处理一致性） --------------------------
def get_cifar10_sample(index_list):
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
    ])
    test_set = datasets.CIFAR10(root='./data', train=False, transform=transform_test, download=False)
    samples = []
    for idx in index_list:
        img_tensor, label = test_set[idx]
        # 反归一化恢复原始图像（用于可视化对比）
        inv_normalize = transforms.Normalize(
            mean=[-0.4914/0.2023, -0.4822/0.1994, -0.4465/0.2010],
            std=[1/0.2023, 1/0.1994, 1/0.2010]
        )
        img_original = inv_normalize(img_tensor).permute(1, 2, 0)
        img_original = torch.clamp(img_original, 0, 1)  # 确保像素值在[0,1]
        samples.append({'original': img_original, 'tensor': img_tensor.unsqueeze(0).to(device), 'label': label})
    return samples

# 读取2张图片（索引可自行修改，此处保持[0,10]示例）
samples = get_cifar10_sample([0, 10])
class_names = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# -------------------------- 3. 特征可视化工具函数（保持原逻辑，确保特征格式统一） --------------------------
def visualize_feature_map(feature_tensor, num_channels=3):
    feature = feature_tensor.squeeze(0).cpu().detach()  # 去除batch维度
    if feature.shape[0] > num_channels:
        feature = feature[:num_channels, :, :]  # 取前3个通道（适配RGB显示）
    # 归一化特征值到[0,1]（消除正负值影响，便于可视化）
    feature_min = feature.min()
    feature_max = feature.max()
    feature_norm = (feature - feature_min) / (feature_max - feature_min + 1e-8)
    # 转HWC格式（matplotlib要求的图像格式）
    if num_channels == 1:
        feature_vis = feature_norm.permute(1, 2, 0).repeat(1, 1, 3)  # 单通道转RGB模拟灰度图
    else:
        feature_vis = feature_norm.permute(1, 2, 0)
    return feature_vis

# -------------------------- 4. 核心修改：调整可视化布局（第一张4阶段，第二张保持3阶段） --------------------------
def plot_sample_features(samples):
    """
    可视化布局：
    - 第1行（第一张图）：原图 → 第二层卷积输出 → 空洞卷积输出 → 平均池化结果（4列）
    - 第2行（第二张图）：原图 → 空洞卷积输出 → 平均池化结果（3列，保持原逻辑）
    """
    # 创建画布：2行，最大列数4（适配第一张图的4阶段）
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    fig.suptitle('CIFAR-10 Feature Visualization (Conv2 → Dilated Conv → Avg Pool)', fontsize=16)
    
    # -------------------------- 第一张图：4阶段可视化（原图→Conv2→Dilated→Pool） --------------------------
    sample1 = samples[0]
    with torch.no_grad():
        model(sample1['tensor'])  # 前向传播，获取各层特征
    
    # 1. 原图
    axes[0, 0].imshow(sample1['original'])
    axes[0, 0].set_title(f'Sample 1\nOriginal Image\nLabel: {class_names[sample1["label"]]}')
    axes[0, 0].axis('off')
    
    # 2. 第二层卷积输出（新增，对应实验模型的第二层结构）
    conv2_feat = visualize_feature_map(model.feature_conv2)
    axes[0, 1].imshow(conv2_feat)
    axes[0, 1].set_title(f'Conv2 Output\nShape: {model.feature_conv2.shape[2:]}\nChannels: 96 (show top 3)')
    axes[0, 1].axis('off')
    
    # 3. 空洞卷积输出（实验核心技术，展示上下文捕捉能力）
    dilated_feat = visualize_feature_map(model.feature_dilated)
    axes[0, 2].imshow(dilated_feat)
    axes[0, 2].set_title(f'Dilated Conv Output\nShape: {model.feature_dilated.shape[2:]}\nDilation=2')
    axes[0, 2].axis('off')
    
    # 4. 平均池化结果（实验要求的池化方式，展示平滑降噪效果）
    pooled_feat = visualize_feature_map(model.feature_pooled)
    axes[0, 3].imshow(pooled_feat)
    axes[0, 3].set_title(f'Avg Pool Output\nShape: {model.feature_pooled.shape[2:]}\nKernel=2×2')
    axes[0, 3].axis('off')
    
    # -------------------------- 第二张图：3阶段可视化（保持原逻辑，对比参考） --------------------------
    sample2 = samples[1]
    with torch.no_grad():
        model(sample2['tensor'])
    
    # 1. 原图
    axes[1, 0].imshow(sample2['original'])
    axes[1, 0].set_title(f'Sample 2\nOriginal Image\nLabel: {class_names[sample2["label"]]}')
    axes[1, 0].axis('off')
    
    # 2. 第二层卷积输出（新增，对应实验模型的第二层结构）
    conv2_feat = visualize_feature_map(model.feature_conv2)
    axes[1, 1].imshow(conv2_feat)
    axes[1, 1].set_title(f'Conv2 Output\nShape: {model.feature_conv2.shape[2:]}\nChannels: 96 (show top 3)')
    axes[1, 1].axis('off')
    
    # 3. 空洞卷积输出
    dilated_feat2 = visualize_feature_map(model.feature_dilated)
    axes[1, 2].imshow(dilated_feat2)
    axes[1, 2].set_title(f'Dilated Conv Output\nShape: {model.feature_dilated.shape[2:]}')
    axes[1, 2].axis('off')
    
    # 4. 平均池化结果
    pooled_feat2 = visualize_feature_map(model.feature_pooled)
    axes[1, 3].imshow(pooled_feat2)
    axes[1, 3].set_title(f'Avg Pool Output\nShape: {model.feature_pooled.shape[2:]}')
    axes[1, 3].axis('off')
    
    
    # 保存并显示
    plt.tight_layout()
    plt.savefig('feature_visualization_updated.png')
    plt.show()

# -------------------------- 5. 执行可视化与模型验证 --------------------------
if __name__ == '__main__':
    plot_sample_features(samples)
    print("可视化完成！已保存为 feature_visualization_updated.png")
    
    # 验证模型加载正确性（可选，确保特征来自训练好的模型）
    print("\n模型预测验证：")
    for idx, sample in enumerate(samples):
        with torch.no_grad():
            output = model(sample['tensor'])
            pred = torch.argmax(output, dim=1).item()
        print(f"Sample {idx+1}: 真实标签={class_names[sample['label']]}, 模型预测={class_names[pred]}")