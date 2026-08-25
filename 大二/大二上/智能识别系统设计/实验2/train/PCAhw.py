from numpy import *
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
def pca(dataMat, topNfeat):
    # 沿着列方向求均值，也就是求出平均点m
    # axis=0 按列方向计算,axis=1按行方向
    meanVals = mean(dataMat,axis=0)
    # 去标准化,每个样本减去平均样本点m
    meanRemoved = dataMat-meanVals
    # 计算R矩阵,转置矩阵左乘原矩阵
    RovMat = np.dot(meanRemoved.T,meanRemoved)
    # 计算矩阵的特征值和特征向量
    eigVals,eigVects = linalg.eig(mat(RovMat))
    # 将特征值从大到小排序，返回的是特征值对应的数组里的下标
    eigValInd = argsort(eigVals)[::-1]
    # 保留最大的前K个特征值
    eigValInd = eigValInd[:topNfeat]
    # 对应R矩阵的特征向量
    redEigVects = eigVects[:, eigValInd]
    # 对应S矩阵的特征向量
    SedEigVects = np.dot(meanRemoved, redEigVects.T)
    # 归一化特征向量
    SedEigVects_normalized = SedEigVects / np.linalg.norm(SedEigVects, axis=0)
    # 原样本矩阵投影到特征向量矩阵P,获得低维矩阵表示
    lowDDataMat = meanRemoved.dot(SedEigVects_normalized.T)

    # 还原原始数据
    reconMat = (lowDDataMat.dot(SedEigVects_normalized)) + meanVals

    # 打印结果
    # print("协方差矩阵:")
    # print(covMat)
    print("标准化后的数据:")
    print(meanRemoved)
    # print("降维后的数据:")
    # print(lowDDataMat)
    print("特征值:")
    print(eigVals[eigValInd])
    print("特征向量:")
    print(redEigVects)
    return lowDDataMat,reconMat,redEigVects

if __name__ == '__main__':
    # # 导入椭圆图像
    # eclipse = cv.imread("test_1.jpg", cv.IMREAD_COLOR)
    # # 转为灰度图
    # eclipse_gray = cv.cvtColor(eclipse, cv.COLOR_BGR2GRAY)
    # # 图像数据转为列向量
    # column_vector = eclipse_gray.flatten().reshape(-1, 1)
    # #
    # best = PCA(n_components=0.95)
    # best.fit(column_vector)
    # best_con = best.n_components_
    # # pca处理，返回维数为18
    # eclipse_reduce = pca(column_vector, best_con)
    # cv.imshow(":", eclipse)
    # cv.waitKey(0)

    # 导入灰色图像
    image = cv.imread("test_2.bmp", cv.IMREAD_COLOR)
    # 转为灰度图
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # 将图像的大小归一化，转化为宽为120，高为90的图像，否则空间不够
    image_gray = cv.resize(image_gray, (120, 90))
    # 图像数据转为列向量
    column_vector = image_gray.flatten().reshape(-1, 1)
    print(column_vector.shape)
    eclipse_reduce = pca(column_vector, 3)

    lowDDataMat, reconMat, redEigVects = pca(column_vector, 3)

    # 显示原始图像
    cv.imshow("Original Image", image)

    # 获取图像中心点坐标
    center = (image.shape[1] // 2, image.shape[0] // 2)

    # 绘制主成分轴
    for i in range(redEigVects.shape[1]):
        eigenvector = redEigVects[:, i]
        # 计算轴的起点和终点坐标
        start_point = center
        end_point = center + (eigenvector * 100).astype(int)  # 根据需要调整轴的长度
        # 转换为元组
        end_point = tuple(end_point.A1)

        # 在原图上绘制主成分轴
        color = (0, 0, 255)  # 设置轴的颜色，这里使用红色
        thickness = 2  # 设置轴的线宽
        cv.arrowedLine(image, start_point, end_point, color, thickness)

    # 显示带有主成分轴的图像
    cv.imshow("Image with Principal Component Axes", image)
    cv.waitKey(0)
    cv.destroyAllWindows()