import torch
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

# Fashion-MNIST类别名称
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.2860,), (0.3530,))
])

train_dataset = datasets.FashionMNIST(
    root = './data', train=True, download=True,transform=transform
)

train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=128, shuffle=True)

# 可视化
images, labels = next(iter(train_loader))
plt.figure(figsize=(10, 4))
for i in range(10):
    plt.subplot(2, 5, i+1)
    plt.imshow(images[i][0].numpy(), cmap='gray')
    plt.title(f"Label: {class_names[labels[i].item()]}")
    plt.axis('off')
plt.tight_layout()
plt.savefig("fashion_mnist_samples128.png")
plt.show()
