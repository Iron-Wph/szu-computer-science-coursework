import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# 生成示例数据
data = np.random.rand(100, 10)

# 运行PCA算法获取特征值
pca = PCA()
pca.fit(data)
eigenvalues = pca.explained_variance_

# 绘制特征值与维度的关系图
plt.plot(range(1, len(eigenvalues) + 1), eigenvalues, marker='o')
plt.xlabel('Dimension')
plt.ylabel('Eigenvalue')
plt.title('Eigenvalues vs. Dimension')
plt.show()

# 寻找拐点
diff = np.diff(eigenvalues)
plt.plot(range(2, len(diff) + 2), diff, marker='o')
plt.xlabel('Dimension')
plt.ylabel('Difference in Eigenvalues')
plt.title('Difference in Eigenvalues vs. Dimension')
plt.show()

# 根据拐点选择最佳维度
elbow_index = np.argmax(diff) + 2  # 加上2是因为diff计算导致维度减少了1
print("Best dimension based on elbow method:", elbow_index)