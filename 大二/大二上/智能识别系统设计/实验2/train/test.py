import cv2
from numpy import *
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# PCA类
class Pca:
    def quick_pca(dataMat, topNfeat=9999999):
        # 沿着列方向求均值，也就是求出平均点m
        # axis=0 按列方向计算,axis=1按行方向
        meanVals = mean(dataMat, axis=1)
        # 去标准化,每个样本减去平均样本点m
        meanRemoved = dataMat - meanVals[:, np.newaxis]
        # 计算R矩阵,转置矩阵左乘原矩阵
        RovMat = np.dot(meanRemoved.T, meanRemoved)
        # 计算矩阵的特征值和特征向量
        eigVals, eigVects = linalg.eig(mat(RovMat))
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
        return lowDDataMat, SedEigVects_normalized

    def pca(dataMat, topNfeat=9999999):
        # 沿着列方向求均值，也就是求出平均点m
        # axis=0 按列方向计算,axis=1按行方向
        meanVals = mean(dataMat, axis=1)
        # 去标准化,每个样本减去平均样本点m
        meanRemoved = dataMat - meanVals[:, np.newaxis]
        # rowvar=0 指输入矩阵的每列代表一个变量，计算是变量之间的协方差
        covMat = np.dot(meanRemoved, meanRemoved.T)
        # 计算矩阵的特征值和特征向量
        eigVals, eigVects = linalg.eig(mat(covMat))
        # 将特征值从大到小排序，返回的是特征值对应的数组里的下标
        eigValInd = argsort(eigVals)[::-1]
        # 保留最大的前K个特征值
        eigValInd = eigValInd[:topNfeat]
        # 对应的特征向量
        redEigVects = eigVects[:, eigValInd]
        # 归一化特征向量, axis==0即一列为一个向量，按每个向量求模
        redEigVects_normalized = redEigVects / np.linalg.norm(redEigVects, axis=0)
        # 原样本矩阵投影到特征向量矩阵P,获得低维矩阵表示
        lowDDataMat = np.dot(meanRemoved.T, redEigVects_normalized)
        print("标准化后的数据:")
        print(meanRemoved)
        print("降维后的数据:")
        print(lowDDataMat)
        print("特征值:")
        print(eigVals[eigValInd])
        print("特征向量:")
        print(redEigVects)
        return lowDDataMat, redEigVects_normalized


# 主函数
if __name__ == '__main__':
    # 读取图像并转换为灰度图像
    image = cv2.imread('test_1.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 对图像进行边缘检测
    edges = cv2.Canny(gray, 50, 150)
    cv2.imshow("边缘检测：", edges)
    cv2.waitKey(100)
    # 寻找轮廓
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # 保留大轮廓
        if len(contour) >= 5:
            ellipse = cv2.fitEllipseDirect(contour)
            # 中心点坐标、实轴与虚轴的长度，椭圆的倾斜角
            center, (major_axis, minor_axis), angle = ellipse

            # 将一维存储的轮廓点转为二维的数组(x,y)，行数为点的个数
            points = contour.reshape(-1, 2)

            # 将轮廓点放入pca中处理，返回对应的特征向量
            points_reduce, points_eigVects = Pca.quick_pca(points, 2)

            # 改变主成分轴的方向
            points_eigVects[:, 0] *= 1

            # 得到实轴，虚轴向量
            real, virtual = 45*points_eigVects[:, 1], 45*points_eigVects[:, 0]

            # 用箭头表示实轴和虚轴的方向
            x, y = np.mean(points, axis=0)

            cv2.arrowedLine(image, (int(x), int(y)), (int(x + real[0]), int(y + real[1])),
                            color=(255, 0, 0), thickness=2, tipLength=0.15)
            cv2.arrowedLine(image, (int(x), int(y)), (int(x + virtual[0]), int(y + virtual[1])),
                            color=(0, 0, 255), thickness=2, tipLength=0.15)


    # 显示绘制结果
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()