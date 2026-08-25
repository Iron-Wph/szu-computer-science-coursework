'''
1.链接摄像头
2.键盘定位
3.识别手势
4.捕捉特征
5.手势分类
6.击键判定输入
7.利用pynput模拟真实键盘输入
'''

import cv2
import pandas
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
from pynput.keyboard import Controller  # 为了使虚拟键盘工作
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier


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

# 创建KNN模型的训练集
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

    return all_hu_moments



# KNN分类器
class KNN_detector:
    # 传入的参数均以列表的形式进行存储
    def __init__(self):
        # # 没有训练集，则调用函数进行生成构建
        # pictures = create_train_Set()

        # 已构建训练集，从文本文件中加载训练集数据
        pictures = np.loadtxt("hu_moments.txt")
        # 读取标签数据
        labels = np.loadtxt("train_labels.txt")


        # 交叉验证法求取最优的K值
        # 绘制带交叉验证的学习曲线
        score = []
        var_ = []
        krange = range(1, 20)

        for k in krange:
            clf = KNeighborsClassifier(n_neighbors=k)
            cvresult = cross_val_score(clf, pictures, labels, cv=5)
            score.append(cvresult.mean())
            var_.append(cvresult.var())

        # # 保存最优分数的索引
        bestindex = pandas.Series(score, index=krange).idxmax()
        best_K = krange[bestindex]

        # 训练KNN模型
        self.knn = KNeighborsClassifier(n_neighbors=best_K)
        # 使用整个训练集进行训练
        self.knn.fit(pictures, labels)

        print("训练成功")

    # 分类预测，传入手部的感兴趣区域ROI
    def predict(self, image):
        # 提取Hu矩特征
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

        # 将Hu矩展平为一维行向量
        hu_moments_vector = hu_moments.flatten()
        # 将一维行向量转换为一维数组
        hu_moments_array = np.array(hu_moments_vector)
        # 将一维数组转换为一维行向量
        hu_moments_row_vector = np.reshape(hu_moments_array, (1, -1))

        # 使用已经训练好的KNN模型进行分类预测
        result = self.knn.predict(hu_moments_row_vector)
        # 返回分类的结果
        return result


# 实现键盘及键位定位
class keyborad_location:
    # 构造函数
    def __init__(self, name, image):
        self.name = name
        self.image = image

    # 定位键盘的每个键的位置，并且返回以字典存储的质心信息（key从1到30）以及列表存储的边框信息
    def locate_key(self):
        # 改变大小
        image = cv2.resize(self.image, (800, 600))
        # 进行双边滤波
        filtered_image = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)

        # 将图像从RGB颜色空间转换为YCrCb颜色空间
        ycrcb_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2YCrCb)
        # 提取Cb通道
        cb_channel = ycrcb_image[:, :, 2]
        # 使用Otsu阈值法进行二值化
        _, cb_binary_image = cv2.threshold(cb_channel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        #
        cv2.imshow("fileted:", filtered_image)
        cv2.imshow("cb_chanel:", cb_binary_image)

        # 定义图像的宽度和高度
        image_width = cb_binary_image.shape[1]
        image_height = cb_binary_image.shape[0]

        # 定义四个顶点的位置
        v1 = [0, 0]
        v2 = [image_width - 1, 0]
        v3 = [0, image_height - 1]
        v4 = [image_width - 1, image_height - 1]

        # 定义直线的截距
        intercept_v1 = 0
        intercept_v2 = image_width - 1
        intercept_v3 = image_height - 1
        intercept_v4 = image_width + image_height - 2

        # 逼近顶点v1和v4
        while cb_binary_image[v1[1], v1[0]] == 0:
            # 碰到上边界，从截距点重新开始
            if v1[1] == 0:
                # 截距加1
                intercept_v1 += 1
                # 初始化新的起点
                v1[1] = intercept_v1
                v1[0] = 0

            # 逼近顶点v1
            v1[0] += 1
            v1[1] = int(-v1[0] + intercept_v1)

        while cb_binary_image[v4[1], v4[0]] == 0:
            # 碰到下边界，从右边界重新开始
            if v4[1] == image_height - 1:
                # 截距减1
                intercept_v4 -= 1
                # 初始化新的起点
                v4[0] = image_width - 1
                v4[1] = int(-v4[0] + intercept_v4)

            # 逼近顶点v4
            v4[0] -= 1
            v4[1] = int(-v4[0] + intercept_v4)

        # 逼近顶点v2和v3
        while cb_binary_image[v2[1], v2[0]] == 0:
            # 碰到上边界，从右边界重新开始
            if v2[1] == 0:
                # 截距减1
                intercept_v2 -= 1
                # 初始化新的起点
                v2[0] = image_width - 1
                v2[1] = int(v2[0] - intercept_v2)

            # 逼近顶点v2
            v2[0] -= 1
            v2[1] = int(v2[0] - intercept_v2)

        while cb_binary_image[v3[1], v3[0]] == 0:
            # 碰到下边界，则从截距点重新开始
            if v3[1] == image_height - 1:
                # 截距减1
                intercept_v3 -= 1
                v3[0] = 0
                v3[1] = intercept_v3

            # 逼近顶点v3
            v3[0] += 1
            v3[1] = int(v3[0] + intercept_v3)

        # 绘制键盘定位结果
        result_image = cv2.cvtColor(cb_binary_image, cv2.COLOR_GRAY2BGR)
        cv2.circle(result_image, tuple(v1), 5, (0, 0, 255), -1)
        cv2.circle(result_image, tuple(v2), 5, (0, 0, 255), -1)
        cv2.circle(result_image, tuple(v3), 5, (0, 0, 255), -1)
        cv2.circle(result_image, tuple(v4), 5, (0, 0, 255), -1)

        # 轮廓检测
        contours, _ = cv2.findContours(cb_binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 过滤轮廓
        filtered_contours = []
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h  # 计算宽高比
            if len(approx) == 4 and aspect_ratio >= 0.5 and aspect_ratio <= 2.0:
                filtered_contours.append(approx)

        # 创建一个空的边界框列表，存储每个键位的边界框（左上角+宽度+高度）
        bounding_boxes = []
        # 创建一个空的键位质心字典
        key_centers = {}

        # 绘制质心和标记
        for i, contour in enumerate(filtered_contours):
            # 计算边界框信息
            x, y, w, h = cv2.boundingRect(contour)
            # 将边界框信息添加到边界框列表中
            bounding_boxes.append((x, y, w, h))

            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(cb_binary_image, (cX, cY), 5, (0, 0, 255), -1)
            # 将质心坐标添加到键位质心字典中
            key_centers[i + 1] = (cX, cY)  # 这里使用键位的编号作为键，质心坐标作为值

        #
        cv2.imshow("result", result_image)
        cv2.imshow("location:", cb_binary_image)
        print(key_centers)
        print(bounding_boxes)
        cv2.waitKey(1)
        # 返回键位的质心以及边框位置信息
        return key_centers, bounding_boxes

# 根据键盘的布局创建一个列表数组，并定义一个空字符串来存储键入的键
keyboard_keys = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",
                 "A", "S", "D", "F", "G", "H", "J", "K", "L", ";",
                 "Z", "X", "C", "V", "B", "N", "M", ",", ".", "del"]
final_text = ""

# 设定计算机的摄像头为图像输入，该IP由DroidCam app进行获取
cap = cv2.VideoCapture("http://192.168.137.52:4747/mjpegfeed")

#设置分辨率为1280*720
cap.set(3, 1280)
cap.set(4, 720)

# 以 0.8 的检测置信度初始化 HandDetector 并将其分配给检测器
detector = HandDetector(detectionCon=0.8)

# 判断是否第一帧
first = False

# 为了使虚拟键盘工作
keyboard = Controller()

# 开始训练KNN分类器
myKNN = KNN_detector()

# 键盘质心信息以及键盘的边框信息
key_centers = {}
bounding_boxes = []

# 主程序入口
if __name__ == "__main__":
    # 开始键盘输入
    while True:
        success, img = cap.read()
        # 检查图像帧是否成功读取，不成功或者读取完则直接结束
        if img is None or not img.any():
            print("图像帧无效")
            break

        # 如果是第一帧，则放入键盘类进行键盘定位
        if not first:
            obj = keyborad_location("keyboard", img)
            key_centers, bounding_boxes = obj.locate_key()
            # 是否成功读取键盘信息
            if len(key_centers) == 30:
                first = True
            # 输出键位的质心信息以及边框信息
            print(key_centers)
            print(bounding_boxes)

        # 键盘定位后，开始识别
        else:
            # 将图像等比例缩放到原来的47%，需要与训练集的保持一致的大小
            scale_percent = 47
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            dim = (width, height)
            img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

            # 在图像中寻找手部信息
            allhands, img = detector.findHands(img)

            # 返回20个手势点的坐标和边界框坐标
            lmlist = []
            bboxInfo = []
            for hand in allhands:
                lmlist.append(hand["lmList"])
                bboxInfo.append(hand["bbox"])

            lmlist = [item for sublist in lmlist for item in sublist]

            # 找到了手部
            if bboxInfo and len(bboxInfo[0]) == 4:
                # 截取手部感兴趣信息
                x = bboxInfo[0][0] - 20
                y = bboxInfo[0][1] - 20
                width = bboxInfo[0][2] + 40
                height = bboxInfo[0][3] + 40
                # 提取感兴趣的区域
                roi = img[y:y + height, x:x + width]

                # 使用KNN分类器进行预测，返回分类结果
                result = KNN_detector.predict(roi)

                # 根据分类结果进行相应的操作
                # 判定为点击手势
                if result == 1:
                    # 提取食指的位置信息
                    cx = lmlist[8][0]
                    cy = lmlist[8][1]

                    # 判断食指指尖的位置在哪个按钮中
                    j = 0
                    while j < 30:
                        # 如果在该键位中
                        if bounding_boxes[j][0] < cx < bounding_boxes[j][0] + bounding_boxes[j][2] and \
                                bounding_boxes[j][1] < cy < bounding_boxes[j][3]:
                            # 判断是否为删除键位
                            if keyboard_keys[j] == "del":
                                count = 1
                                if count == 1:
                                    if len(final_text) > 0:
                                        # 删除最后一个字符
                                        final_text = final_text[:-1]
                                        # 模拟键盘输入删除键
                                        keyboard.press(keyboard._Key.backspace)
                                        keyboard.release(keyboard._Key.backspace)
                                    # 设定间隔时间，避免多次选择删除键
                                    sleep(0.2)
                                    count = 0
                            # 输入字符的按键
                            else:
                                count = 1
                                if count == 1:
                                    # 模拟按键
                                    keyboard.press(keyboard_keys[j])
                                    # 添加新文本
                                    final_text += keyboard_keys[j]
                                    # 设定间隔时间，避免多次选择删除键
                                    sleep(0.2)
                                    count = 0
                        j += 1

        # 显示图像
        cv2.imshow("keyboard", img)
        cv2.waitKey(1)
        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
