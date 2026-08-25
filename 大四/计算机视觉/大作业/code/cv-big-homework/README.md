# 肺炎感染影像智能识别系统

## 项目简介
本项目是一个基于深度学习的肺炎感染影像智能识别系统，通过预训练的AlexNet、GoogleNet和VGG19三种卷积神经网络模型对肺部影像进行分类，判断是否为肺炎阳性。系统提供了直观的GUI界面，方便用户上传影像并查看各模型的识别结果。

**也可以自己选择其他模型进行训练分类，作为创新点加分项**

## 环境要求
- Python 3.7+
- 依赖库：
  - torch
  - torchvision
  - PIL (Pillow)
  - tkinter
  - numpy
  - matplotlib
  - scikit-learn
  - pandas
  - tqdm

## 安装步骤
1. 克隆或下载项目代码到本地
2. 安装依赖库：
```bash
pip install torch torchvision Pillow numpy matplotlib scikit-learn pandas tqdm
```
3. 确保模型文件存在于以下路径（需自行训练或获取预训练模型）：
   - `alex/alex.pth`
   - `google/google.pth`
   - `vgg/vgg.pth`

## 使用说明
1. 运行GUI程序：
```bash
python gui.py
```
2. 操作步骤：
   - 点击"选择图像"按钮，上传待识别的肺部影像（支持jpg、png格式）
   - 点击"CNN识别"按钮，系统将使用三种模型进行识别并显示结果
   - 识别结果将在表格中展示，包括各模型及融合模型的判断结果
   - 点击"退出系统"按钮关闭程序

## 项目结构
```
cv-big-homework/
├── gui.py               # 主程序，包含GUI界面和识别逻辑
├── evaluate.py          # 模型评估脚本，生成混淆矩阵
├── analyze_network.py   # 网络结构分析脚本
├── alex/
│   ├── train_alex.py    # AlexNet训练脚本
│   └── alex.pth         # AlexNet模型文件
├── google/
│   ├── train_google.py  # GoogleNet训练脚本
│   └── google.pth       # GoogleNet模型文件
├── vgg/
│   ├── train_vgg.py     # VGG19训练脚本
│   └── vgg.pth          # VGG19模型文件
└── dbs/                 # 数据集目录（需自行准备）
    ├── 肺炎阳性/        # 肺炎阳性样本
    └── 肺炎阴性/        # 肺炎阴性样本
```

## 模型训练
如需重新训练模型，可分别运行各模型的训练脚本：
```bash
# 训练AlexNet
python alex/train_alex.py

# 训练GoogleNet
python google/train_google.py

# 训练VGG19
python vgg/train_vgg.py
```
训练数据需按照`dbs/类别/图像`的结构存放，训练脚本会自动划分训练集和验证集（默认9:1）

## 模型评估
运行评估脚本可生成各模型及融合模型的混淆矩阵：
```bash
python evaluate.py
```
评估结果将以图片形式保存，包括各模型的混淆矩阵（保存于对应模型目录）和融合模型的混淆矩阵（保存于根目录）
