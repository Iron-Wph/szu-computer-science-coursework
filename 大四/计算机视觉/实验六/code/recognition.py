from torchvision.transforms import transforms
from char_segment import char_segment, char_segment2
from train_cnn import CNN
from gen_yzm import gen_yzm
import torch
import numpy as np
import cv2


def preprocess(crops):
    # 数据转换
    trans = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ])

    # 对数据进行转换
    crops = [trans(cv2.resize(c, (28, 28))[:, :, ::-1].copy()).unsqueeze(0) for c in crops]

    # 合并为tensor
    crops = torch.cat(crops)
    return crops


def recognition(image, model, show=False):
    # 类别标签
    cls2idx = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11,
               'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'J': 18, 'K': 19, 'L': 20, 'M': 21, 'N': 22,
               'P': 23, 'Q': 24, 'R': 25, 'S': 26, 'T': 27, 'U': 28, 'V': 29, 'W': 30, 'X': 31, 'Y': 32, 'Z': 33}
    idx2cls = {v: k for k, v in cls2idx.items()}

    # 对图像进行分割
    crops, boxes, orig_image = char_segment(image)
    # 数据预处理
    crops_tensor = preprocess(crops)

    # 模型预测
    preds = model(crops_tensor)
    # 获取预测类别
    preds_cls = []
    for pred in preds:
        idx = torch.argmax(pred)
        c = idx2cls[int(idx)]
        preds_cls.append(c)
    # print(preds_cls)

    if show:
        for box, c in zip(boxes, preds_cls):
            x, y, w, h = box
            cv2.rectangle(orig_image, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.putText(orig_image, c, (x, y), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 0, 255), 1)

        cv2.imshow('result', orig_image)
        cv2.waitKey()
    return preds_cls, crops


def recognition2(image, model, show=False):
    # 类别标签
    cls2idx = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '8': 5, '9': 6, 'A': 7, 'B': 8, 'C': 9, 'D': 10, 'E': 11, 'F': 12, 'G': 13, 'H': 14, 'J': 15, 'K': 16, 'L': 17, 'M': 18, 'N': 19, 'P': 20, 'R': 21, 'S': 22, 'T': 23, 'W': 24, 'X': 25, 'Y': 26}
    idx2cls = {v: k for k, v in cls2idx.items()}

    # 对图像进行分割
    crops, boxes, orig_image = char_segment2(image)
    # 数据预处理
    crops_tensor = preprocess(crops)

    # 模型预测
    preds = model(crops_tensor)
    # 获取预测类别
    preds_cls = []
    for pred in preds:
        idx = torch.argmax(pred)
        c = idx2cls[int(idx)]
        preds_cls.append(c)
    # print(preds_cls)

    return preds_cls, crops


if __name__ == '__main__':
    image = gen_yzm("6aBf")

    # 加载模型
    model = CNN()
    model.load_state_dict(torch.load('model.pth'))
    model.eval()

    recognition(image, model, show=True)
