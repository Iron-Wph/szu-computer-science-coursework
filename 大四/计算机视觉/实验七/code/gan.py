import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import PIL.Image
import numpy as np
import matplotlib.pyplot as plt


class CartoonDataset(Dataset):
    """
    自定义卡通头像数据集类
    """

    def __init__(self, root_dir, transform=None):
        """
        参数:
            root_dir: 包含卡通头像的目录
            transform: 图像预处理变换
        """
        self.root_dir = root_dir
        self.transform = transform
        self.image_files = [f for f in os.listdir(root_dir)
                            if f.endswith(('.png', '.jpg', '.jpeg'))]

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_path = os.path.join(self.root_dir, self.image_files[idx])
        image = PIL.Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image


# 数据预处理管道
data_transform = transforms.Compose([
    transforms.Resize(64),  # 统一图像尺寸
    transforms.CenterCrop(64),
    transforms.ToTensor(),  # 转换为Tensor
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # 归一化到[-1,1]
])


def create_dataloader(data_dir, batch_size=256):
    dataset = CartoonDataset(data_dir, transform=data_transform)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    return dataloader


# 权重初始化函数
def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        nn.init.normal_(m.weight.data, 0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        nn.init.normal_(m.weight.data, 1.0, 0.02)
        nn.init.constant_(m.bias.data, 0)

# 生成器定义


class Generator(nn.Module):
    def __init__(self, nz=100, ngf=64, nc=3):
        """
        参数:
                    nz:
        噪声向量维度
                    ngf:
                    nc:
        生成器特征图深度
        输出图像通道数(RGB为3)
        """
        super(Generator, self).__init__()
        self.main = nn.Sequential(
            # 输入: nz x 1 x 1
            nn.ConvTranspose2d(nz, ngf * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(ngf * 8),
            nn.ReLU(True),
            # 状态: (ngf*8) x 4 x 4
            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),
            # 状态: (ngf*4) x 8 x 8
            nn.ConvTranspose2d(ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),
            # 状态: (ngf*2) x 16 x 16
            nn.ConvTranspose2d(ngf * 2, ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),
            nn.ConvTranspose2d(ngf, nc, 4, 2, 1, bias=False),
            nn.Tanh()
            # 状态: (nc) x 64 x 64
        )

    def forward(self, input):
        return self.main(input)

# 判别器定义


class Discriminator(nn.Module):
    def __init__(self, nc=3, ndf=64):
        super(Discriminator, self).__init__()
        self.main = nn.Sequential(
            # 输入: (nc) x 64 x 64
            nn.Conv2d(nc, ndf, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            # 状态: (ndf) x 32 x 32
            nn.Conv2d(ndf, ndf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 2),
            nn.LeakyReLU(0.2, inplace=True),
            # 状态: (ndf*2) x 16 x 16
            nn.Conv2d(ndf * 2, ndf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 4),
            nn.LeakyReLU(0.2, inplace=True),
            # 状态: (ndf*4) x 8 x 8
            nn.Conv2d(ndf * 4, ndf * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 8),
            nn.LeakyReLU(0.2, inplace=True),
            # 状态: (ndf*8) x 4 x 4
            nn.Conv2d(ndf * 8, 1, 4, 1, 0, bias=False),
            nn.Sigmoid()
            # 状态: 1 x 1 x 1
        )

    def forward(self, input):
        return self.main(input).view(-1, 1).squeeze(1)


class GANTrainer:
    def __init__(self, data_dir, nz=100, device='cuda'):
        self.device = device
        self.nz = nz
        self.netG = Generator(nz).to(device)
        self.netD = Discriminator().to(device)
        # 初始化权重
        self.netG.apply(weights_init)
        self.netD.apply(weights_init)

        # 定义损失函数和优化器
        self.criterion = nn.BCELoss()
        self.optimizerG = optim.Adam(
            self.netG.parameters(), lr=0.0002, betas=(0.5, 0.999))
        self.optimizerD = optim.Adam(
            self.netD.parameters(), lr=0.0002, betas=(0.5, 0.999))
        # 准备数据
        self.dataloader = create_dataloader(data_dir)
        # 固定噪声用于训练过程中可视化
        self.fixed_noise = torch.randn(64, nz, 1, 1, device=device)
        # 记录训练过程
        self.G_losses = []
        self.D_losses = []
        self.img_list = []

    def train(self, num_epochs=100):
        print("开始训练...")
        for epoch in range(num_epochs):
            for i, data in enumerate(self.dataloader, 0):
                # 训练判别器 
                self.netD.zero_grad() 
                real_images = data.to(self.device) 
                batch_size = real_images.size(0) 
                real_labels = torch.full((batch_size,), 1.0, device=self.device) 
                output = self.netD(real_images) 
                errD_real = self.criterion(output, real_labels) 
                errD_real.backward() 
                D_x = output.mean().item() 
                # 使用生成图像训练 
                noise = torch.randn(batch_size, self.nz, 1, 1, device=self.device) 
                fake_images = self.netG(noise) 
                fake_labels = torch.full((batch_size,), 0.0, device=self.device) 
                output = self.netD(fake_images.detach()) 
                errD_fake = self.criterion(output, fake_labels) 
                errD_fake.backward() 
                D_G_z1 = output.mean().item()
                errD = errD_real + errD_fake 

                self.optimizerD.step() 
                # 训练生成器 
                self.netG.zero_grad() 
                real_labels.fill_(1.0)  
                # 生成器希望判别器将假图像判断为真 
                output = self.netD(fake_images) 
                errG = self.criterion(output, real_labels) 
                errG.backward() 
                D_G_z2 = output.mean().item() 
                self.optimizerG.step()
                
                # 记录损失
                if i % 50 == 0:
                    self.G_losses.append(errG.item())
                    self.D_losses.append(errD.item())
                # 输出训练状态
                if i % 100 == 0:
                    print(f'[{epoch}/{num_epochs}][{i}/{len(self.dataloader)}] '
                          f'Loss_D: {errD.item():.4f} Loss_G: {errG.item():.4f} '
                          f'D(x): {D_x:.4f} D(G(z)): {D_G_z1:.4f} / {D_G_z2:.4f}')
            # 每个epoch结束后使用固定噪声生成图像
            with torch.no_grad():
                fake = self.netG(self.fixed_noise).detach().cpu()
                self.img_list.append(fake)
            # 保存检查点
            if epoch % 10 == 0:
                torch.save({
                    'epoch': epoch,
                    'generator_state_dict': self.netG.state_dict(),
                    'discriminator_state_dict': self.netD.state_dict(),
                    'optimizerG_state_dict': self.optimizerG.state_dict(),
                    'optimizerD_state_dict': self.optimizerD.state_dict(),
                    'G_losses': self.G_losses,
                    'D_losses': self.D_losses,
                }, f'checkpoint_epoch_{epoch}.pth')
        print("训练完成!")

    def plot_training_progress(self):
        plt.figure(figsize=(10, 5))
        plt.title("生成器和判别器损失")
        plt.plot(self.G_losses, label="G")
        plt.plot(self.D_losses, label="D")
        plt.xlabel("迭代次数")
        plt.ylabel("损失")
        plt.legend()
        plt.savefig("gan_loss.png")
        plt.show()


if __name__ == "__main__":
    trainer = GANTrainer(data_dir='./dbs/faces')
    trainer.train(num_epochs=100)
    trainer.plot_training_progress()
