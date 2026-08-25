import torch 
import torch.nn as nn
from torchinfo import summary

class CNNWithBatchNorm(nn.Module):
    def __init__(self):
        super(CNNWithBatchNorm, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=5,padding=2)
        self.bn1 = nn.BatchNorm2d(16)
        self.relu = nn.ReLU()
        self.pool = nn.AvgPool2d(kernel_size=2,stride=2)
        # self.pool = nn.MaxPool2d(kernel_size=2,stride=2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=5, padding=2)
        self.bn2 = nn.BatchNorm2d(32)
        self.fc = nn.Linear(32*7*7,10)
    
    def forward(self,x ):
        x = self.conv1(x)
        x = self.bn1(x)  # 应⽤BN
        x = self.relu(x)
        x = self.pool(x)
        x = self.conv2(x)
        x = self.bn2(x)  # 应⽤BN
        x = self.relu(x)
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

# 可视化参数网络
model = CNNWithBatchNorm()
summary(
    model,
    input_size = (1,1,28,28),
    col_names=["input_size", "output_size", "num_params"],
    col_width=20 
)