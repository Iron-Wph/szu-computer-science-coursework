'''
1.链接摄像头
2.识别手势
3.绘制键盘
 3.1创建键盘字母List
 3.2通过循环绘制键盘
4.根据坐标，取得返回字母
 4.1 利用lmList[8]食指之间坐标，判断选中的字母
 4.2 利用食指与中指之间的距离，确认输入的字母
 5.扩展，修改键盘背景
 6.利用pynput模拟真实键盘输入
'''

import cv2
import cvzone
import math
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
from time import sleep
import numpy as np
from pynput.keyboard import Controller  #为了使虚拟键盘工作

# 以 0.8 的检测置信度初始化 HandDetector 并将其分配给检测器
detector = HandDetector(detectionCon=0.8)

# 根据键盘的布局创建一个列表数组，并定义一个空字符串来存储键入的键
keyboard_keys = [["Q","W","E","R","T","Y","U","I","O","P"],
                 ["A","S","D","F","G","H","J","K","L",";"],
                 ["Z","X","C","V","B","N","M",",",".","del"]]
final_text = ""

# 为了使虚拟键盘工作
keyboard = Controller()


# 绘制键盘（实心）
# 接受两个参数（图像和按钮列表），并返回图像
def draw(img,buttonlist):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size

        # 在每个键的角落绘制矩形边缘。这是为了让我们的键盘布局看起来更好看
        cvzone.cornerRect(img, (button.pos[0], button.pos[1],
                                button.size[0], button.size[0]), 20, rt=0)
        cv2.rectangle(img,(int(x),int(y)), (int(x + w), int(y + h)), (255, 144, 30), cv2.FILLED)

        # 位置参数：1.图片 2.需显示的文字 3.文字添加到图片的位置 4.字体类型 5.字体大小 6.字体颜色 7.字体粗细
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
    return img


def transparent_layout(img,buttonlist):
    imgNew = np.zeros_like(img,np.uint8)
    for button in buttonlist:
        x,y = button.pos

        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[0]), 20, rt=0)
        cv2.rectangle(imgNew, (int(x),int(y)), (int(x + button.size[0]), int(y + button.size[1])), (255, 144, 30), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

    # 复制一份图像
    out = img.copy()

    alpaha = 0.5
    mask = imgNew.astype(bool)

    # 图像融合：1.图像1  2.图像1的权重  3.图像2 4.图像2的权重 5.融合后，每个像素点加的标量
    out[mask] = cv2.addWeighted(img,alpaha,imgNew,1-alpaha,0)[mask]
    return out

# 定义按键的属性
class Button():
    def __init__(self,pos,text,size=[85,85]):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []
for k in range(len(keyboard_keys)):
    # 遍历列表元素
    for x, key in enumerate(keyboard_keys[k]):
        # 增加元素到列表的末尾
        buttonList.append(Button([100*x+25,100*k+50],key))



if __name__ == '__mian__':
    # 设定计算机的摄像头为图像输入
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    # 设置分辨率为1280*720
    cap.set(3, 1280)
    cap.set(4, 720)

    while True:
        success, img = cap.read()
        if not cap.isOpened():
            print("摄像头没有成功打开！")
        else:
            # 镜像处理
            img = cv2.flip(img, 1)
            # 只在图像中寻找手
            allhands, img = detector.findHands(img)

            # 返回20个手势点的坐标和边界框坐标
            lmlist = []
            bboxInfo = []
            for hand in allhands:
                lmlist.append(hand["lmList"])
                bboxInfo.append(hand["bbox"])

            lmlist = [item for sublist in lmlist for item in sublist]

            # 添加键盘图层
            img = transparent_layout(img, buttonList)

            # lmList为手部节点坐标
            if lmlist:
                # s
                print(lmlist)
                for button in buttonList:
                    x, y = button.pos
                    w, h = button.size
                    #
                    print(f"食指坐标：{lmlist[8][0]}+{lmlist[8][1]}")
                    print(f"按钮坐标：{x}+{y}")

                    # lmList[8]为食指指尖坐标，lmList[12]为中指指尖坐标
                    if x < lmlist[8][0] < x + w and y < lmlist[8][1] < y + h:

                        cv2.rectangle(img, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 255), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

                        l, info, _ = detector.findDistance((lmlist[8][0], lmlist[8][1]), (lmlist[12][0], lmlist[12][1]),
                                                           img)

                        cv2.putText(img, f"distance:{l}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                        print(f"l:{l}")
                        if l < 40:
                            if button.text == "del":
                                count = 1
                                if count == 1:
                                    if len(final_text) > 0:
                                        # keyboard.press(keyboard_keys)
                                        # 删除最后一个字符
                                        final_text = final_text[:-1]
                                        # 模拟键盘输入删除键
                                        keyboard.press(keyboard._Key.backspace)
                                        keyboard.release(keyboard._Key.backspace)

                                    # 设定间隔时间，避免多次选择删除键
                                    sleep(0.2)
                                    count = 0

                            else:
                                count = 1
                                if count == 1:
                                    keyboard.press(button.text)

                                    # 用户UI反馈，选中后修改字体和底部矩形颜色
                                    cv2.rectangle(img, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 0),
                                                  cv2.FILLED)
                                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4,
                                                (0, 0, 0), 4)
                                    final_text += button.text

                                    # 设定间隔时间，避免多次选择同一字母
                                    sleep(0.2)
                                    count = 0

            # 输入结果显示于图像
            cv2.rectangle(img, (25, 350), (700, 450), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, final_text, (60, 425), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

            cv2.imshow("keyboard", img)
            # 快捷键按下‘q’退出程序
            if cv2.waitKey(1) == ord('q'):
                break
    # 程序技术
    cap.release()
    cv2.destroyAllWindows()

