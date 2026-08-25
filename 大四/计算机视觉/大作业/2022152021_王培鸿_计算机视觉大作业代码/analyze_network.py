import netron
import torch
import os

from torch import nn
from torchvision.models import alexnet, googlenet, vgg19


def analyze_network(model, input_shape=(1, 3, 224, 224)):
    x = torch.randn(input_shape)
    torch.onnx.export(model, x, 'tmp.pth')
    netron.start('tmp.pth')


# model = alexnet()
# model.classifier = nn.Sequential(
# nn.Dropout(p=0.5),
# nn.Linear(256 * 6 * 6, 4096),
# nn.ReLU(inplace=True),
# nn.Dropout(p=0.5),
# nn.Linear(4096, 4096),
# nn.ReLU(inplace=True),
# nn.Linear(4096, 2),)
#
# analyze_network(model)

# model = googlenet()
# # model.classifier = nn.Sequential(
# # nn.Dropout(p=0.5),
# # nn.Linear(256 * 6 * 6, 4096),
# # nn.ReLU(inplace=True),
# # nn.Dropout(p=0.5),
# # nn.Linear(4096, 4096),
# # nn.ReLU(inplace=True),
# # nn.Linear(4096, 2),)
# model.fc = nn.Linear(1024, 2)

# analyze_network(model)

model = vgg19()
model.classifier = nn.Sequential(
nn.Linear(512 * 7 * 7, 4096),
nn.ReLU(True),
nn.Dropout(p=0.5),
nn.Linear(4096, 4096),
nn.ReLU(True),
nn.Dropout(p=0.5),
nn.Linear(4096, 2),)

analyze_network(model)
