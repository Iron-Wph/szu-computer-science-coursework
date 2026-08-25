from numpy import *
import numpy as np
def pca(dataMat,topNfeat=9999999):
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
    redEigVects = eigVects[:,eigValInd]
    # 归一化特征向量, axis==0即一列为一个向量，按每个向量求模
    redEigVects_normalized = redEigVects / np.linalg.norm(redEigVects, axis=0)
    # 原样本矩阵投影到特征向量矩阵P,获得低维矩阵表示
    lowDDataMat =np.dot(meanRemoved.T, redEigVects_normalized)
    
    # 打印结果
    print("标准化后的数据:")
    print(meanRemoved)
    print("特征值:")
    print(eigVals[eigValInd])
    print("特征向量:")
    print(redEigVects)
    return lowDDataMat


if __name__ == '__main__':
    # 输入数据
    data = np.array([[0.01, 0.68],
                     [0.33, 0.74],
                     [0.16, 0.45],
                     [0.79, 0.08],
                     [0.31, 0.22],
                     [0.52, 0.91],
                     [0.16, 0.15],
                     [0.6, 0.82],
                     [0.26, 0.53],
                     [0.65, 0.9]])
    lowDMat = pca(data.T, 2)
    print("\n")
