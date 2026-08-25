from numpy import *
import numpy as np
def pca(dataMat,topNfeat=9999999):
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
    eigVals,eigVects = linalg.eig(mat(RovMat))
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

    # 还原原始数据
    # reconMat = (lowDDataMat.dot(SedEigVects_normalized)) + meanVals

    # 打印结果
    # print("协方差矩阵:")
    # print(covMat)
    print(meanVals)
    print("标准化后的数据:")
    print(meanRemoved)
    print("R:")
    print(RovMat)
    print("R的特征值:")
    print(eigVals[eigValInd])
    print("R的特征向量:")
    print(redEigVects)
    print("S的特征向量:")
    print(SedEigVects)
    print("降维后的数据:")
    print(lowDDataMat)
    return lowDDataMat


if __name__ == '__main__':
    # 输入数据
    # data = np.array([[0.01, 0.68],
    #                  [0.33, 0.74],
    #                  [0.16, 0.45],
    #                  [0.79, 0.08],
    #                  [0.31, 0.22],
    #                  [0.52, 0.91],
    #                  [0.16, 0.15],
    #                  [0.6, 0.82],
    #                  [0.26, 0.53],
    #                  [0.65, 0.9]])
    # lowDMat = pca(data,2)
    data = np.array([[0.23, 0.35, 0.82],
                     [0.01, 0.04, 0.16],
                     [0.64, 0.73, 0.64],
                     [0.45, 0.54, 0.29]
                     ])
    lowDMat = pca(data, 3)