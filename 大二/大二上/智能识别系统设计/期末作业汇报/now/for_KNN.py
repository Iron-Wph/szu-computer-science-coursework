import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score, train_test_split
import pandas


# # 打开文件以供写入
# file = open("labels.txt", "w")
#
#
# for i in range(1, 11):
#     for j in range(1, 41):
#         # 将整数变量转换为字符串，并写入文件
#         file.write(str(i)+"\n")
#
#
# # 关闭文件
# file.close()

# 样本矩阵，样本标签
X = np.loadtxt("Eigen Values.txt")
# y = np.genfromtxt("labels.txt", dtype=str)
y = np.loadtxt("labels.txt")
print(X.shape)
print(y.shape)

# 绘制K值的学习曲线
# 拆分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=233)

scores = []
best_k, best_score = 0, 0

krange = range(1, 20, 1)
for k in krange:
    clf = KNeighborsClassifier(n_neighbors=k)  # n_neighbors：取邻近点的个数k
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    # 记录每个K值下的分数
    scores.append(score)
    # 记录最优的K值和对应的分数
    if score > best_score:
        best_score = score
        best_k = k

# 输出最优的K值及分数，绘制K值的学习曲线
print(f"最优的K值：{best_k}")
print(f"最优的准确率：{best_score}")
plt.plot(krange, scores)
plt.savefig("学习曲线.jpg")
plt.show()


# # 绘制带交叉验证的学习曲线
# score = []
# var_ = []
# krange = range(1, 20)
#
# for k in krange:
#     clf = KNeighborsClassifier(n_neighbors=k)
#     cvresult = cross_val_score(clf, X, y, cv=5)
#     score.append(cvresult.mean())
#     var_.append(cvresult.var())
#
# plt.plot(krange, score, color='k')
# plt.plot(krange, np.array(score) + np.array(var_) * 2, c='red', linestyle='--')
# plt.plot(krange, np.array(score) - np.array(var_) * 2, c='red', linestyle='--')
# plt.xlabel('K')
# plt.ylabel('Accuracy')
# plt.title('Cross Validation for K in KNN')
# # 保存最优分数的索引
# bestindex = pandas.Series(score, index=krange).idxmax()
# best_K = krange[bestindex]
#
# plt.savefig("KNN_交叉验证.jpg")
# plt.show()
# # 输出
# print(f"best_k:{best_K}")
# print(f"best_score:{score[bestindex]}")




best_k, best_p, best_score = 0, 0, 0


k_values = list(range(2, 11))
accuracy_scores = []
for k in range(2, 11):  # 外层循环搜索k
    scores_for_k = []  # 保存每个k值下的准确率
    for p in range(1, 6):  # 内层循环搜索p
        knn = KNeighborsClassifier(weights="distance", n_neighbors=k, p=p)
        scores = cross_val_score(knn, X_train, y_train, cv=3)  # 3折交叉验证
        score = np.mean(scores)  # 当前这一组超参数在验证集上的平均分
        scores_for_k.append(score)
        if score > best_score:
            best_k, best_p, best_score = k, p, score
    accuracy_scores.append(scores_for_k)  # 添加每个k值下的准确率列表

accuracy_scores = np.array(accuracy_scores)  # 转换为NumPy数组

# 可视化结果
for i, k in enumerate(k_values):
    plt.plot(range(1, 6), accuracy_scores[i], marker='o', label=f'k={k}')  # 绘制每个k值下的曲线

plt.xlabel('p')
plt.ylabel('Accuracy')
plt.title('Cross Validation for p in KNN')
plt.legend()
plt.show()

# 加载训练数据和标签
train_sample = np.loadtxt("Eigect Values.txt")
labels = np.genfromtxt("labels.txt", dtype=str)
# X = np.array([[2, 3], [3, 5], [4, 6], [7, 8]])
# y = np.array([0, 0, 1, 1])

# 设置k值的范围
k_values = list(range(1, 10))

# 交叉验证求解最佳k值
accuracy_scores = []
for k in k_values:
	knn = KNeighborsClassifier(n_neighbors=k)
	scores = cross_val_score(knn, train_sample, labels, cv=3)  # 3折交叉验证
	accuracy_scores.append(scores.mean())

# 可视化结果
plt.plot(k_values, accuracy_scores, marker='o')
plt.xlabel('k')
plt.ylabel('Accuracy')
plt.title('Cross Validation for k in KNN')
plt.savefig("KNN_交叉验证.jpg")
plt.show()

# 找到最佳k值
best_k = k_values[np.argmax(accuracy_scores)]
print("Best k value:", best_k)
