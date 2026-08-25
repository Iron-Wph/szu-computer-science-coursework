import cv2
import cvzone
import math
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
from time import sleep
import numpy as np
from pynput.keyboard import Controller  # 为了使虚拟键盘工作

# 以 0.8 的检测置信度初始化 HandDetector 并将其分配给检测器
detector = HandDetector(detectionCon=0.8)

#
i = 1
while i <= 10:
    # 读取图像
    image = cv2.imread(f"./train_set/{i}.jpg")
    #
    allhands, image = detector.findHands(image)

    # #
    # bboxInfo = []
    #
    # # 获取手部de回归框的信息
    # for hand in allhands:
    #     bboxInfo.append(hand["bbox"])
    #
    # # 截取感兴趣区域信息
    # x = bboxInfo[0][0] - 20
    # y = bboxInfo[0][1] - 20
    # width = bboxInfo[0][2] + 40
    # height = bboxInfo[0][3] + 40
    #
    # roi = image[x:x + width, y:y + height]
    # # 图像大小归一化为(120, 90)
    # roi = cv2.resize(roi, (120, 90))
    #
    # # 显示裁剪的原图像
    # cv2.imshow("src", roi)

    # 转换为Cb通道，进行大津法的背景分割
    # 将图像从RGB颜色空间转换为YCrCb颜色空间
    ycrcb_image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

    ycrcb_image = cv2.resize(ycrcb_image, (800, 600))
    # 提取Cb通道
    cb_channel = ycrcb_image[:, :, 2]
    cr_channel = ycrcb_image[:, :, 1]
    # 使用Otsu阈值法进行二值化
    _, cb_binary_image = cv2.threshold(cb_channel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, cr_binary_image = cv2.threshold(cr_channel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # 显示图像
    cv2.imshow("Otsu,", cb_binary_image)

    cv2.imwrite(f"roi{i}.jpg", ycrcb_image)
    cv2.imwrite(f"cb_otsu{i}.jpg", cb_binary_image)
    cv2.imwrite(f"cr_otsu{i}.jpg", cr_binary_image)
    i += 1

    cv2.waitKey(10)


