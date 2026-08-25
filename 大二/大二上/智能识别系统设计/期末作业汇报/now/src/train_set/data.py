import cv2, numpy as np
from cvzone.HandTrackingModule import HandDetector

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

# 以 0.8 的检测置信度初始化 HandDetector 并将其分配给检测器
detector = HandDetector(detectionCon=0.8)

# 读取训练图片
timg = cv2.imread(f"{5}(1).jpg")
# timg = cv2.resize(timg)
# 截取手部图像，并归一化大小
allhands, timg = detector.findHands(timg)
bboxInfo = []
# 获取手部de回归框的信息
for hand in allhands:
    bboxInfo.append(hand["bbox"])

print(bboxInfo)
# 截取感兴趣区域信息
x = bboxInfo[0][0]-20
y = bboxInfo[0][1]-20
width = bboxInfo[0][2] + 40
height = bboxInfo[0][3] + 40

#
cv2.rectangle(timg, (x, y), (x+width, y+height), (0, 0, 0), 2)
cv2.imshow("src", timg)
roi = timg[y:y+height, x:x+width]
cv2.imshow("roi", roi)
# 图像大小归一化为(120, 90)
# roi = cv2.resize(roi, (120, 90))
# 数据增强预处理
rois_stronger = data_stronger(roi)

scale_percent = 50
for i in range(0, 7):
    image = rois_stronger[i]
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    cv2.imshow(f"{i}", image)

cv2.waitKey(0)