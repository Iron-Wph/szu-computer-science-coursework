import cv2
import numpy as np
import pandas
from cvzone.HandTrackingModule import HandDetector
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd

# 数据增强，用于构建训练集
def data_stronger(image):
    res = []
    res.append(image)
    # 顺时针、逆时针45度
    center = (image.shape[1] / 2.0, image.shape[0] / 2.0)
    rotationMatrix = cv2.getRotationMatrix2D(center, -45, 1.0)
    rotatedImage1 = cv2.warpAffine(image, rotationMatrix, (image.shape[1], image.shape[0]))
    rotationMatrix = cv2.getRotationMatrix2D(center, 45, 1.0)
    rotatedImage2 = cv2.warpAffine(image, rotationMatrix, (image.shape[1], image.shape[0]))
    res.append(rotatedImage1)
    res.append(rotatedImage2)

    # 垂直镜像
    mirroredImage = cv2.flip(image, 0)
    res.append(mirroredImage)

    # 增强颜色通道
    redhancedImage = image.copy()
    bluehancedImage = image.copy()
    greenhancedImage = image.copy()

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # 蓝色处理
            pixel0 = bluehancedImage[i, j]
            pixel0[0] = np.uint8(np.clip(int(pixel0[0]) + 100, 0, 255))  # 调整增强强度
            # 绿色处理
            pixel1 = greenhancedImage[i, j]
            pixel1[1] = np.uint8(np.clip(int(pixel1[1]) + 100, 0, 255))  # 调整增强强度
            # 红色处理
            pixel2 = redhancedImage[i, j]
            pixel2[2] = np.uint8(np.clip(int(pixel2[2]) + 100, 0, 255))  # 调整增强强度

    res.append(redhancedImage)
    res.append(bluehancedImage)
    res.append(greenhancedImage)

    return res

def create_train_Set():
    # 以 0.8 的检测置信度初始化 HandDetector 并将其分配给检测器
    detector = HandDetector(detectionCon=0.8)

    # 创建一个空列表来存储所有样本的Hu矩
    all_hu_moments = []

    # 构建训练集合
    for j in range(1, 11):
        # 读取训练图片
        timg = cv2.imread(f"./train_set/{j}.jpg")

        # 缩放图像至原来的47%
        scale_percent = 47
        width = int(timg.shape[1] * scale_percent / 100)
        height = int(timg.shape[0] * scale_percent / 100)
        dim = (width, height)
        timg = cv2.resize(timg, dim, interpolation=cv2.INTER_AREA)

        # 截取手部图像，并归一化大小
        allhands, timg = detector.findHands(timg)
        bboxInfo = []
        # 获取手部de回归框的信息
        for hand in allhands:
            bboxInfo.append(hand["bbox"])

        print(bboxInfo)
        # 截取感兴趣区域信息
        x = bboxInfo[0][0] - 20
        y = bboxInfo[0][1] - 20
        width = bboxInfo[0][2] + 40
        height = bboxInfo[0][3] + 40

        roi = timg[y:y + height, x:x + width]
        cv2.imshow("roi", roi)

        # 将roi进行数据增强
        result = data_stronger(roi)

        # 遍历每一张图像进行二值化并提取hu矩特征
        for i in range(0, 7):
            # 提取图像
            image = result[i]
            # 将图像从RGB颜色空间转换为YCrCb颜色空间
            ycrcb_image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
            # 提取Cr通道
            cr_channel = ycrcb_image[:, :, 1]
            # 使用Otsu阈值法进行二值化
            _, cr_binary_image = cv2.threshold(cr_channel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # 计算图像的Hu矩
            moments = cv2.moments(cr_binary_image)

            hu_moments = cv2.HuMoments(moments).flatten()

            # 打印Hu矩
            print(hu_moments)
            # 将Hu矩添加到列表中
            all_hu_moments.append(hu_moments)

    # # 将Hu矩列表写入到文件中
    # with open("hu_moments.txt", "w") as file:
    #     for hu_moments in all_hu_moments:
    #         line = " ".join(str(value) for value in hu_moments)
    #         file.write(line + "\n")


    # 将Hu矩列表转换为DataFrame
    df = pd.DataFrame(all_hu_moments)

    # 将DataFrame写入Excel文件
    df.to_excel('hu_moments.xlsx', index=False)
    cv2.waitKey(10)


# 主函数区域
if __name__ == "__main__":
    # 读取图片创建训练集合
    create_train_Set()

    # # 从文本文件中加载训练集数据
    # hu_moments_matrix = np.loadtxt("hu_moments.txt")
    # # 读取标签数据
    # labels = np.loadtxt("train_labels.txt")
    #
    #
    #
    # # 将数据分为训练集和测试集
    # X_train, X_test, y_train, y_test = train_test_split(hu_moments_matrix, labels, test_size=0.2, random_state=42)
    #
    # # 创建KNN分类器并训练模型
    # knn = KNeighborsClassifier(n_neighbors=3)
    # knn.fit(X_train, y_train)
    #
    # # 绘制带交叉验证的学习曲线
    # score = []
    # var_ = []
    # krange = range(1, 20)
    #
    # for k in krange:
    #     clf = KNeighborsClassifier(n_neighbors=k)
    #     cvresult = cross_val_score(clf, hu_moments_matrix, labels, cv=5)
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
    # # 在测试集上进行预测
    # y_pred = knn.predict(X_test)
    #
    # # 计算分类准确率
    # accuracy = np.mean(y_pred == y_test)
    # print("Accuracy:", accuracy)