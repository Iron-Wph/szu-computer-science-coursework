import cv2
import numpy as np
import matplotlib.pyplot as plt


def compute_covariance_matrix(Xm):
    # 计算协方差矩阵
    num_samples = Xm.shape[0]
    S = np.dot(Xm.T, Xm) / (num_samples - 1)
    return S


def pca(Xm, num_components):
    # 主成分分析
    # 对数据进行中心化
    Xm_centered = Xm - np.mean(Xm, axis=0)
    S = compute_covariance_matrix(Xm_centered)
    eigenvalues, eigenvectors = np.linalg.eig(S)
    idx = np.argsort(eigenvalues)[::-1]
    top_eigenvalues = eigenvalues[idx][:num_components]
    top_eigenvectors = eigenvectors[:, idx][:, :num_components]

    for i in range(num_components):
        top_eigenvectors[:, i] /= np.linalg.norm(top_eigenvectors[:, i])

    # 打印特征值和特征向量
    print("特征值:")
    print(top_eigenvalues)
    print("特征向量:")
    print(top_eigenvectors)

    return top_eigenvectors


# 读取图像
image = cv2.imread('test_1.jpg')

# 转换为灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 对图像进行高斯模糊以获得更好的边缘检测效果
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 调整Canny边缘检测参数
edges = cv2.Canny(blurred, 30, 100)

# 寻找轮廓
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    # 过滤掉小轮廓
    if len(contour) >= 5:
        # 使用fitEllipseDirect进行椭圆拟合，获得更好的结果
        ellipse = cv2.fitEllipseDirect(contour)

        center, axes, angle = ellipse
        major_axis, minor_axis = axes

        print(f"中心点: {center}, 主轴长度: {major_axis}, 次轴长度: {minor_axis}, 角度: {angle}")

        points = contour.reshape(-1, 2)
        top_eigenvectors = pca(points, num_components=2)

        # 改变主成分轴的方向
        top_eigenvectors[:, 0] *= 1

        scale = 30
        x, y = np.mean(points, axis=0)
        v1, v2 = scale * top_eigenvectors[:, 1], scale * top_eigenvectors[:, 0]

        print("type v1:", type(v1[0]))
        cv2.ellipse(image, ellipse, color=(0, 255, 0), thickness=2)

        # 以箭头形式表示主成分轴
        cv2.arrowedLine(image, (int(x), int(y)), (int(x + v1[0]), int(y + v1[1])),
                        color=(255, 0, 0), thickness=2, tipLength=0.1)
        cv2.arrowedLine(image, (int(x), int(y)), (int(x + v2[0]), int(y + v2[1])),
                        color=(0, 0, 255), thickness=2, tipLength=0.1)

# 显示结果
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.show()
