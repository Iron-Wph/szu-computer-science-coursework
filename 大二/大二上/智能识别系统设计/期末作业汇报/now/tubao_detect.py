import cv2, numpy as np
from cvzone.HandTrackingModule import HandDetector


# 以 0.8 的检测置信度初始化 HandDetector 并将其分配给检测器
detector = HandDetector(detectionCon=0.8)

# 读取训练图片
timg = cv2.imread(f"./train_set/{5}(1).jpg")
image = timg.copy()
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

roi = timg[y:y+height, x:x+width]
cv2.imshow("roi", roi)

# 将图像从RGB颜色空间转换为YCrCb颜色空间
ycrcb_image = cv2.cvtColor(roi, cv2.COLOR_BGR2YCrCb)

# 提取Cr通道
cr_channel = ycrcb_image[:, :, 1]
# 使用Otsu阈值法进行二值化
_, cr_binary_image = cv2.threshold(cr_channel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#
img = cr_binary_image
cv2.imshow("", img)


# # 边缘检测
# edges = cv2.Canny(cr_binary_image, threshold1=30, threshold2=100)  # 使用Canny边缘检测算法
# # 寻找轮廓
# contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# # 选择最大的轮廓
# largest_contour = max(contours, key=cv2.contourArea)
# # 检测凸包
# convex_hull = cv2.convexHull(largest_contour)
# # 绘制凸包
# cv2.drawContours(cr_binary_image, [convex_hull], 0, (255, 255, 255), thickness=2)
# # 显示结果图像
# cv2.imshow("Convex Hull", cr_binary_image)
#
# i = 0
# for point in convex_hull:
#     # 提取凸包点的特征，例如坐标、距离等
#     print(point)
#     i+=1
# print(i)

# 计算图像的Hu矩
moments = cv2.moments(cr_binary_image)
hu_moments = cv2.HuMoments(moments)

# 打印Hu矩
for i in range(7):
    print(f"Hu Moment {i+1}: {hu_moments[i][0]}")

cv2.waitKey(0)
cv2.destroyAllWindows()