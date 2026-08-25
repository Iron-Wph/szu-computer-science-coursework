import torch.nn as nn
class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        # 第一个卷积层
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3,stride=1,padding=1)
        self.bn1 = nn.BatchNorm2d(64)   
        self.relu = nn.ReLU(inplace=True)
        # 第二个卷积层
        self.conv2 = nn.Conv2d(in_channels=64, out_channels=96, kernel_size=3,stride=1,padding=1)
        self.bn2 = nn.BatchNorm2d(96)
        # 第三个卷积层（空洞卷积）
        self.conv3_dilated = nn.Conv2d(in_channels=96, out_channels=128, kernel_size=3,dilation=2,padding=2)
        self.bn3 = nn.BatchNorm2d(128)
        # 池化层
        self.avg_pool = nn.AvgPool2d(kernel_size=2, stride=2)        
        self.global_avg_pool = nn.AdaptiveAvgPool2d((1, 1)) 
        # 正则化层
        self.dropout = nn.Dropout(0.3)
        # 全连接层
        self.fc = nn.Linear(128, 10)        
    
    def forward(self, x):
        # 记录关键层输出（用于可视化）
        self.feature_conv1 = self.relu(self.bn1(self.conv1(x)))  # conv1输出
        self.feature_conv2 = self.relu(self.bn2(self.conv2(self.feature_conv1)))  # conv2输出
        self.feature_dilated = self.relu(self.bn3(self.conv3_dilated(self.feature_conv2)))  # 空洞卷积输出
        self.feature_pooled = self.avg_pool(self.feature_dilated)  # 平均池化后输出
        x = self.global_avg_pool(self.feature_pooled)
        x = x.view(x.size(0), -1)       
        x = self.dropout(x)
        x = self.fc(x)
        return x