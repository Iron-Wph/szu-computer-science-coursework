
import torch
from torch import nn
from torch import optim
import torchvision
from torchvision.models import alexnet, AlexNet_Weights
from tqdm import tqdm
from torch.utils.data import DataLoader, Dataset
from torchvision.datasets import ImageFolder
from torchvision.transforms import transforms
from pathlib import Path
import random
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


def split_data(data_dir='验证码数据集/dbc', train_size=0.9, seed=0):
    random.seed(seed)

    data_dir = Path(data_dir)
    cls = [p.stem for p in data_dir.glob('*')]
    cls.sort()
    cls2idx = {c: i for i, c in enumerate(cls)}
    train_set = []
    val_set = []
    for c in cls:
        cls_dir = data_dir / c
        images = list(cls_dir.glob('*.jpg'))
        random.shuffle(images)

        n_train = int(train_size * len(images))
        train_images = images[:n_train]
        val_images = images[n_train:]

        train_labels = [c] * n_train
        val_labels = [c] * (len(images) - n_train)

        train_set.extend(list(zip(train_images, train_labels)))
        val_set.extend(list(zip(val_images, val_labels)))
    return train_set, val_set, cls2idx


class DataSet(Dataset):
    def __init__(self, data, cls2idx, transform):
        self.data = data
        self.cls2idx = cls2idx
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        image = Image.open(self.data[item][0]).convert('RGB')
        image = self.transform(image)
        cls = self.cls2idx[self.data[item][1]]
        return image, cls


class CNN(nn.Module):
    def __init__(self, num_classes=34):
        super(CNN, self).__init__()

        # 第一个卷积层
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        # 第二个卷积层
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        # 第三个卷积层
        self.conv3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.bn3 = nn.BatchNorm2d(64)
        self.relu3 = nn.ReLU()
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)

        # 第四个卷积层
        self.conv4 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)
        self.bn4 = nn.BatchNorm2d(128)
        self.relu4 = nn.ReLU()
        self.pool4 = nn.MaxPool2d(kernel_size=2, stride=2)

        # 全连接分类层
        self.fc = nn.Linear(128 * 1 * 1, num_classes)  # 输入大小根据卷积层的设置而定

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu1(x)
        x = self.pool1(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu2(x)
        x = self.pool2(x)

        x = self.conv3(x)
        x = self.bn3(x)
        x = self.relu3(x)
        x = self.pool3(x)

        x = self.conv4(x)
        x = self.bn4(x)
        x = self.relu4(x)
        x = self.pool4(x)

        # 将特征图展平为一维向量
        x = x.view(x.size(0), -1)

        # 全连接分类层
        x = self.fc(x)

        return x


def main():
    epochs = 25
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    lr = 1e-3
    wd = 1e-5

    batch_size = 64
    num_workers = 0

    train_data, val_data, cls2idx = split_data(data_dir='验证码数据集/dbc', train_size=0.9)

    train_set = DataSet(train_data, cls2idx, transform=transforms.Compose([
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ]))
    val_set = DataSet(val_data, cls2idx, transform=transforms.Compose([
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ]))

    train_loader = DataLoader(train_set, batch_size=batch_size,
                              shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(val_set, batch_size=batch_size,
                            shuffle=True, num_workers=num_workers)
    def train_one_epoch():
        model.train()
        correct = 0
        total = 0
        train_logger = tqdm(train_loader)
        total_loss = 0
        total_acc = 0
        for i, (images, labels) in enumerate(train_logger):
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            accuracy = 100 * correct / total
            total_acc += accuracy

            train_logger.set_description(f"Epoch {epoch}/{epochs}")
            train_logger.set_postfix_str(f'train loss: {total_loss / (i + 1):.5f} train acc:{total_acc / (i + 1):.2f}%')

        return total_loss / (i + 1), total_acc / (i + 1)

    def val_one_epoch():
        model.eval()
        correct = 0
        total = 0
        total_loss = 0
        total_acc = 0
        val_logger = tqdm(val_loader, colour='WHITE')
        with torch.no_grad():
            for i, (images, labels) in enumerate(val_logger):
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                total_loss += loss.item()

                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                accuracy = 100 * correct / total
                total_acc += accuracy

                val_logger.set_description(f"\t\tval")
                val_logger.set_postfix_str(f'val loss: {total_loss / (i + 1):.5f} val acc:{total_acc / (i + 1):.2f}%')

        return total_loss / (i + 1), total_acc / (i + 1)

    # 加载模型
    model = CNN()
    model.to(device)

    # 损失函数
    criterion = nn.CrossEntropyLoss().to(device)
    # 优化器
    optimizer = optim.SGD(model.parameters(), lr=lr, weight_decay=wd)

    # 训练指标
    metrics = []
    # 进行迭代训练
    for epoch in range(1, epochs + 1):
        train_loss, train_acc = train_one_epoch()
        val_loss, val_acc = val_one_epoch()
        metrics.append((train_loss, train_acc, val_loss, val_acc))

        torch.save(model.state_dict(), '课堂练习6-1代码/model_25.pth')

    metrics = np.array(metrics)

    # 绘制评估信息
    fig, ax = plt.subplots(1, 2, figsize=(18, 6))

    ax[0].plot(metrics[:, 1], label='Training accuracy')
    ax[0].plot(metrics[:, 3], label='Validation accuracy')
    ax[0].set_xlabel('Epoch')
    ax[0].set_ylabel('Accuracy')
    ax[0].legend()
    ax[0].grid()

    ax[1].plot(metrics[:, 0], label='Training loss')
    ax[1].plot(metrics[:, 2], label='Validation loss')
    ax[1].set_xlabel('Epoch')
    ax[1].set_ylabel('Loss')
    ax[1].legend()
    ax[1].grid()
    plt.savefig('metrics25.jpg')
    # plt.show()


if __name__ == '__main__':
    main()

