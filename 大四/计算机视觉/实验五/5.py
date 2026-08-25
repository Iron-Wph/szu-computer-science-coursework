import torch 
import torch.nn as nn 
from torchvision import models, transforms, datasets 
import matplotlib.pyplot as plt 
from PIL import Image 
import numpy as np 
# 1. 加载CIFAR-10子集作为示例数据库（100张图像） 
transform = transforms.Compose([ 
    transforms.Resize((224, 224)), 
    transforms.ToTensor(), 
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]) 
]) 
dataset = datasets.CIFAR10(root='./data', train=True, download=True, 
transform=transform) 
# 取前100张图像作为数据库 
database_images = [dataset[i][0] for i in range(100)] 
database_labels = [dataset[i][1] for i in range(100)] 
# 2. 加载预训练VGG16（仅使用特征提取部分） 
model = models.vgg16(pretrained=True) 
model.classifier = nn.Identity()  # 移除分类头，仅保留特征提取 

print("before modified: ", model)
# 修改VGG16的特征提取部分，只保留前9层
model.features = torch.nn.Sequential(*list(model.features.children())[:9])
print("after modified: ", model)

model.eval() 
# 3. 提取数据库图像特征 
database_features = [] 
with torch.no_grad(): 
    for img in database_images: 
        feature = model(img.unsqueeze(0))  # 添加batch维度 
        database_features.append(feature.squeeze()) 
database_features = torch.stack(database_features) 

# 4. 定义检索函数：计算查询图像与数据库的余弦相似度
def search_similar_images(query_image, database_features, database_images, 
top_k=3): 
    with torch.no_grad(): 
        query_feature = model(query_image.unsqueeze(0)).squeeze() 
    # 计算余弦相似度 
    similarities = torch.cosine_similarity(query_feature.unsqueeze(0), 
        database_features, dim=1) 
    top_scores, top_indices = torch.topk(similarities, top_k) 
    return top_indices, top_scores 

# 5. 测试：从数据库中选择一张图像作为查询 
# query_idx = 0 
# query_img = database_images[query_idx] 
query_img = Image.open("./data/images/01.jpg").convert('RGB')
query_img = transform(query_img)
top_indices, top_scores = search_similar_images(query_img, database_features, 
database_images) 
 # 6. 可视化结果 
plt.figure(figsize=(10, 5)) 
plt.subplot(1, 4, 1) 
plt.imshow(query_img.permute(1, 2, 0) * 0.5 + 0.5)  # 反标准化显示 
plt.title("search photo") 
plt.axis('off') 
for i, (idx, score) in enumerate(zip(top_indices, top_scores)): 
    plt.subplot(1, 4, i+2) 
    plt.imshow(database_images[idx].permute(1, 2, 0) * 0.5 + 0.5) 
    plt.title(f"similarity: {score:.2f}") 
    plt.axis('off') 
save_name = "vgg16_retrieval.png" 
plt.savefig(save_name, dpi=200, bbox_inches='tight') 