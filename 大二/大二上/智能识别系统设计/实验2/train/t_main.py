from numpy import *
import cv2 as cv
import os
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# 全局变量
best_con = 0  # 最佳降维数值
foldername = ["1_BlurFace", "2_ClifBar", "3_David", "4_Dudek", "5_FaceOcc1", "6_FaceOcc2", "7_FleetFace", "8_Girl",
              "9_Jumping", "10_Mhyang"]


# 手搓的pca快速函数
# dataMat为输入数据集，topNfeat为降维数
def pca(dataMat, topNfeat=9999999):
    # 沿着列方向求均值，也就是求出平均点m
    # axis=0 按列方向计算,axis=1按行方向
    meanVals = mean(dataMat, axis=1)
    # 去标准化,每个样本减去平均样本点m
    meanRemoved = dataMat - meanVals[:, np.newaxis]
    # rowvar=0 指输入矩阵的每列代表一个变量，计算是变量之间的协方差
    # cov()计算协方差矩阵
    covMat = np.dot(meanRemoved, meanRemoved.T)
    # covMat = cov(meanRemoved.T,rowvar=0)
    # 计算矩阵的特征值和特征向量
    eigVals,eigVects = linalg.eig(mat(covMat))

    # 将特征值从大到小排序，返回的是特征值对应的数组里的下标
    eigValInd = argsort(eigVals)[::-1]

    # 保留最大的前K个特征值
    eigValInd = eigValInd[:topNfeat]

    # 对应的特征向量
    redEigVects = eigVects[:, eigValInd]

    # 归一化特征向量, axis==0即一列为一个向量，按每个向量求模
    redEigVects_normalized = redEigVects / np.linalg.norm(redEigVects, axis=0)

    # 原样本矩阵投影到特征向量矩阵P,获得低维矩阵表示
    lowDDataMat =np.dot(meanRemoved.T, redEigVects_normalized)
    # 还原原始数据
    # reconMat = (lowDDataMat.dot(redEigVects_normalized.T)) + meanVals
    return lowDDataMat


def Quick_pca(dataMat,topNfeat=9999999):
    # 沿着列方向求均值，也就是求出平均点m
    # axis=0 按列方向计算,axis=1按行方向
    meanVals = mean(dataMat, axis=1)
    # 去标准化,每个样本减去平均样本点m
    # meanVals = meanVals.T
    # print(dataMat.shape[1])
    meanRemoved = dataMat - meanVals[:, np.newaxis]
    # meanRemoved = dataMat - meanVals
    # 计算R矩阵,转置矩阵左乘原矩阵
    RovMat = np.dot(meanRemoved.T, meanRemoved)

    # 计算矩阵的特征值和特征向量
    eigVals, eigVects = linalg.eig(mat(RovMat))
    # print("tezhengshi:")
    # print(eigVals)
    # 将特征值从大到小排序，返回的是特征值对应的数组里的下标
    eigValInd = argsort(eigVals)[::-1]
    # 保留最大的前K个特征值
    eigValInd = eigValInd[:topNfeat]
    # 对应R矩阵的特征向量
    redEigVects = eigVects[:, eigValInd]

    # 对应S矩阵的特征向量
    SedEigVects = np.dot(meanRemoved, redEigVects)

    # 归一化特征向量, axis==0即一列为一个向量，按每个向量求模
    SedEigVects_normalized = SedEigVects / np.linalg.norm(SedEigVects, axis=0)
    # 原样本矩阵投影到特征向量矩阵P,获得低维矩阵表示
    lowDDataMat = np.dot(meanRemoved.T, SedEigVects_normalized)
    # # 还原原始数据
    # reconMat = (lowDDataMat.dot(SedEigVects_normalized)) + meanVals

    return lowDDataMat, SedEigVects_normalized, meanVals


# 创建训练样本
def create_train():
    # 依次读取各个大小统一后的训练图片，将图片转为1维列向量后合成大矩阵X
    j = 0
    # 合成大矩阵X
    X = np.empty((120 * 90, 0))
    # 对应的列标签y
    y = []
    while j <= 9:
        i = 1
        while i <= 10:
            file = f"trainset/{foldername[j]}/{i}.jpg"
            image = cv.imread(file, 0)
            column_vector = image.flatten().reshape(-1, 1)
            X = np.hstack((X, column_vector))
            i += 1
        j += 1
        y.extend([j] * 10)

    # 标签y先转换为numpy数组
    y = np.array(y)

    # # 输出矩阵X
    # print("矩阵X:")
    # print(X)
    # # 输出矩阵X的维数
    # print("矩阵X的维数:")
    # print(X.shape)
    # # 输出标签y
    # print(y)
    return X, y


# 计算每类样本的平均距离
def count_distance(dataMat):
    # 计算降维后的数据的每个类的均值向量，即每10个为一类求均值，存于dist列表中
    dist = []
    # 将矩阵 reshape 成 (10, 10, 5) 的形状
    reshaped_mat = dataMat.reshape(10, 10, -1)
    # 计算每个子矩阵的均值，沿着第一个轴（行）求均值
    dist = np.mean(reshaped_mat, axis=1)
    # print("输出均值：", dist)
    # print("junzhi weidu:", dist.shape)
    return dist


# 构建检测分类函数，传参为计算好的每类均值列表
def predict(distance, eigvects, average_Set):
    # 构建人脸检测器，若构建不成功直接结束
    cascade = cv.CascadeClassifier()
    if not cascade.load("haarcascade_frontalface_default.xml"):
        print("Failed to load cascade file.")

    # num[]数组存储每类测试样本的数量
    num = [293, 272, 420, 845, 592, 612, 407, 300, 163, 1290]

    # detect[]数组用于保存每类样本的识别正确概率
    detects = []

    # 逐帧提取测试图像
    j = 0
    for j in range(0, 10):
        detect = 0
        sum = num[j]
        i = 1
        while i <= sum:
            filename = f"testset/{foldername[j]}/test/({i}).jpg"
            i += 1
            image = cv.imread(filename, cv.IMREAD_COLOR)  # 以原彩色图像读取
            # 转换为灰度图像
            image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            # 识别人脸
            faces = cascade.detectMultiScale(image_gray, 1.3, 2, 0, (50, 50))

            # 如果识别出人脸，否则输出图像后直接下一帧
            if len(faces) != 0:
                # 框出人脸
                face_image = []
                for (x, y, w, h) in faces:
                    cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    face_image = image_gray[y:y + h, x:x + w]
                    # 将提取出的人脸的大小归一化
                    face_image = cv.resize(face_image, (120, 90))

                # 将列表转换为NumPy数组
                face_image_array = np.array(face_image)

                # 使用flatten()方法将多维数组转换为一维数组
                column_vector = face_image_array.flatten().reshape(-1, 1)

                # 先将其减去平均脸
                print("column_vector:", column_vector.shape)
                print(type(column_vector))

                row_average_Set = average_Set.flatten().reshape(-1, 1)
                print(type(row_average_Set))
                print("平均点:", average_Set.T.shape)
                column_vector = column_vector - row_average_Set

                # 先将训练样本转为 1*d 维度
                column_vector = column_vector.T
                # row_face = column_vector.T
                print("column_vector:", column_vector.T.shape)

                # 将人脸数据通过特征向量矩阵投影到子空间
                test_reduce = np.dot(column_vector, eigvects)

                print("测试数据的维度为：", test_reduce.shape)
                k = 1
                label = 0
                mindist = 10000000
                # 分类贴标签处理，分类法2：一共10个类的均值向量
                for k in range(0, 10):
                    dispt = np.linalg.norm(test_reduce - distance[k], axis=1)
                    if mindist > dispt:
                        mindist = dispt
                        label = k
                    print("距离：", dispt)

                print("min dispt :", mindist)
                print("label num:", label)
                # 输出分类结果
                print(f"label:{foldername[label]}")
                # 如果分类正确，分类正确结果加1
                if label == j:
                    detect += 1

                # 在图像上输出标签
                label_text = f"{foldername[label]}"
                label_position = (x, y - 10)  # 在人脸框上方一些位置显示标签
                font = cv.FONT_HERSHEY_SIMPLEX
                font_scale = 0.8
                color = (0, 255, 0)  # (B, G, R)
                thickness = 2
                cv.putText(image, label_text, label_position, font, font_scale, color, thickness)

            # 显示图像，无论是否带有标签
            cv.imshow("Labeled Image", image)
            cv.waitKey(10)

        # 计算该类样本的识别正确率
        correct = (1.0 * detect) / num[j]
        # 输出该类样本的识别正确率
        print(f"{foldername[j]}的识别正确率为：{correct * 100}%")
        # 将这个分类识别正确率存入分类中，调用append()方法不断插入列表末尾
        detects.append(correct)

    print("每类的识别率依次为: ")
    for j in range(0, 10):
        print(f"{j + 1}:{detects[j] * 100}% ")


import matplotlib.pyplot as plt
# 手肘法计算降维维度
def testweidu(data):
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


def contrib(data_matrix):
    # 假设你已经加载了数据并存储在变量data_matrix中，形状为(样本数, 特征数)
    # 使用PCA进行降维
    pca = PCA()
    pca.fit(data_matrix)

    # 获取每个主成分对原始特征的贡献度
    contribution = np.abs(pca.components_)

    # 计算每个主成分的总贡献度
    total_contribution = np.sum(contribution, axis=1)

    # 绘制主成分贡献度图
    plt.bar(range(1, len(total_contribution) + 1), total_contribution)
    plt.xlabel('Principal Component')
    plt.ylabel('Contribution')
    plt.title('Contribution of Principal Components to Original Features')
    plt.show()


# 主函数
if __name__ == '__main__':
    # 通过调用函数获取训练集合以及标签集合
    train_Set, labels = create_train()

    print("trainset:", train_Set.shape)
    print("labels", labels.shape)

    # # 调用sklearn中的PCA判断设定阈值[0-1.0]降维的最优维度
    # best = PCA(n_components=0.95)
    # best.fit(train_Set)
    # best_con = best.n_components_
    # print("最佳维度为")
    # print(best_con)
    train_Set_reduce = []
    train_Set_EigVects = []
    #
    best_con = 92
    # 如果训练样本存在就不重复构建保存样本
    if os.path.exists("train_Set_reduce.txt"):
        # 从样本文件中加载数据
        train_Set_reduce = np.genfromtxt("train_Set_reduce.txt", dtype=complex)
        train_Set_EigVects = np.genfromtxt("train_Set_EigVects.txt", dtype=complex)
        mean_train_Set = np.genfromtxt("train_Set_mean.txt", dtype=complex)
    # 若本地样本不存在则调用pca创建保存
    else:
        # 根据最佳维度调用pca函数
        # 得到降维后的训练样本和特征向量
        train_Set_reduce, train_Set_EigVects, mean_train_Set = Quick_pca(train_Set, best_con)
        print("tezhegxlsads :", train_Set_EigVects.shape)
        # 降维后的数据以及对应的投影向量矩阵保存到本地中
        np.savetxt("train_Set_reduce.txt", train_Set_reduce)
        np.savetxt("train_Set_EigVects.txt", train_Set_EigVects)
        np.savetxt("train_Set_mean.txt", mean_train_Set)
        print("已保存到本地")

    # 输出矩阵train_Set_reduce的维数
    print("矩阵train_Set_reduce的维数:")
    print(train_Set_reduce.shape)
    # # 输出训练样本矩阵
    # print("训练样本为:")
    # print(train_Set_reduce)

    # 计算每类样本的均值
    train_Set_Distance = count_distance(train_Set_reduce)

    # 调用predict()开始测试图像，传入样本均值计算均值距离以及特征向量矩阵将样本投影到子空间
    predict(train_Set_Distance, train_Set_EigVects, mean_train_Set)

