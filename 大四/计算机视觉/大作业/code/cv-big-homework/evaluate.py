import random
from pathlib import Path
import torch
from PIL import Image
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision.transforms import transforms
from torchvision.models import alexnet, googlenet, vgg19
import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn.utils.multiclass import unique_labels
import matplotlib


plt.rcParams['font.sans-serif'] = ['SimHei']
# matplotlib.use('tkagg')
matplotlib.use('Agg')


def split_data(data_dir='../datasets/dbs', train_size=0.9, seed=0):
    random.seed(seed)

    data_dir = Path(data_dir)
    cls = [p.stem for p in data_dir.glob('*')]
    cls2idx = {c: i for i, c in enumerate(cls)}
    train_set = []
    val_set = []
    for c in cls:
        cls_dir = data_dir / c
        images = list(cls_dir.glob('*'))
        random.shuffle(images)

        n_train = int(train_size * len(images))
        train_images = images[:n_train]
        val_images = images[n_train:]

        train_labels = [c] * n_train
        val_labels = [c] * (len(images) - n_train)

        train_set.extend(list(zip(train_images, train_labels)))
        val_set.extend(list(zip(val_images, val_labels)))

    return train_set, val_set, cls2idx


def eval(model):
    model.eval()

    targets = []
    preds = []

    with torch.no_grad():
        for i, (images, labels) in enumerate(val_loader):
            images = images.to(device)
            outputs = model(images)

            labels = labels.detach().cpu().numpy().tolist()

            _, predicted = torch.max(outputs.data, 1)
            predicted = predicted.detach().cpu().numpy().tolist()

            targets.extend(labels)
            preds.extend(predicted)

    correct = np.sum(np.array(targets) == np.array(preds))
    acc = correct / len(targets)
    print(acc)

    m = confusion_matrix(targets, preds, normalize='true')
    fig, ax = plt.subplots()
    ax.matshow(m, cmap='Blues')
    for i in range(len(m)):
        for j in range(len(m)):
            plt.annotate(round(m[j, i], 2), xy=(
                i, j), horizontalalignment='center', verticalalignment='center')

    ax.set_ylabel('True label')
    ax.set_xlabel('Predicted label')
    ax.set_xticks([0, 1], labels=['Pneumonia Positive',
                  'Pneumonia Negative'], fontsize=10)
    ax.set_yticks([0, 1], labels=['Pneumonia Positive',
                  'Pneumonia Negative'], fontsize=10)

    # ax.set_xticks([0, 1], labels=['肺炎阳性', '肺炎阴性'], fontsize=10)
    # ax.set_yticks([0, 1], labels=['肺炎阳性', '肺炎阴性'], fontsize=10)


def eval_fuse():
    alex.eval()
    google.eval()
    google.eval()

    targets = []
    preds = []

    with torch.no_grad():
        for i, (images, labels) in enumerate(val_loader):
            images = images.to(device)

            # 获取三个模型的预测结果
            alex_outputs = alex(images)
            _, predicted = torch.max(alex_outputs.data, 1)
            alex_predicted = predicted.detach().cpu().numpy().tolist()

            google_outputs = google(images)
            _, predicted = torch.max(google_outputs.data, 1)
            google_predicted = predicted.detach().cpu().numpy().tolist()

            vgg_outputs = vgg(images)
            _, predicted = torch.max(vgg_outputs.data, 1)
            vgg_predicted = predicted.detach().cpu().numpy().tolist()

            predicted = []
            for a, g, v in zip(alex_predicted, google_predicted, vgg_predicted):
                # 众数
                zs = 1 if sum([a, g, v]) >= 2 else 0
                # 对类别0迁移vgg结果
                if zs == 0:
                    zs = v

                predicted.append(zs)

            labels = labels.detach().cpu().numpy().tolist()

            targets.extend(labels)
            preds.extend(predicted)

    correct = np.sum(np.array(targets) == np.array(preds))
    acc = correct / len(targets)
    print(acc)

    m = confusion_matrix(targets, preds, normalize='true')
    fig, ax = plt.subplots()
    ax.matshow(m, cmap='Blues')
    for i in range(len(m)):
        for j in range(len(m)):
            plt.annotate(round(m[j, i], 2), xy=(
                i, j), horizontalalignment='center', verticalalignment='center')

    ax.set_ylabel('True label')
    ax.set_xlabel('Predicted label')
    ax.set_xticks([0, 1], labels=['Pneumonia Positive',
                  'Pneumonia Negative'], fontsize=10)
    ax.set_yticks([0, 1], labels=['Pneumonia Positive',
                  'Pneumonia Negative'], fontsize=10)

    # ax.set_xticks([0, 1], labels=['肺炎阳性', '肺炎阴性'], fontsize=10)
    # ax.set_yticks([0, 1], labels=['肺炎阳性', '肺炎阴性'], fontsize=10)


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


_, val_data, cls2idx = split_data()
device = 'cuda' if torch.cuda.is_available() else 'cpu'

val_set = DataSet(val_data, cls2idx, transform=transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
]))

val_loader = DataLoader(val_set, batch_size=32, shuffle=True, num_workers=0)

# 评估alexnet
alex = alexnet()
alex.classifier = nn.Sequential(
    nn.Dropout(p=0.5),
    nn.Linear(256 * 6 * 6, 4096),
    nn.ReLU(inplace=True),
    nn.Dropout(p=0.5),
    nn.Linear(4096, 4096),
    nn.ReLU(inplace=True),
    nn.Linear(4096, 2),
)
alex.eval()
alex.load_state_dict(torch.load(
    '/data1/wph/final/cv-big-homework/alex/alex_70_0.0003.pth'))
alex.to(device)

eval(alex)
plt.savefig("alex/confusion_matrix.png")
plt.show()

# 评估googlenet
google = googlenet(aux_logits=False, transform_input=True)
google.fc = nn.Linear(1024, 2)
google.eval()
google.load_state_dict(torch.load(
    '/data1/wph/final/cv-big-homework/google/google_70_0.0003.pth'))
google.to(device)

eval(google)
plt.savefig("google/confusion_matrix.png")
plt.show()

# 评估vggnet
vgg = vgg19()
vgg.classifier = nn.Sequential(
    nn.Linear(512 * 7 * 7, 4096),
    nn.ReLU(True),
    nn.Dropout(p=0.5),
    nn.Linear(4096, 4096),
    nn.ReLU(True),
    nn.Dropout(p=0.5),
    nn.Linear(4096, 2),
)
vgg.eval()
vgg.load_state_dict(torch.load(
    '/data1/wph/final/cv-big-homework/vgg/vgg_100_0.0001.pth'))
vgg.to(device)

eval(vgg)
plt.savefig("vgg/confusion_matrix.png")
plt.show()

eval_fuse()
plt.savefig("fuse_confusion_matrix.png")
plt.show()
