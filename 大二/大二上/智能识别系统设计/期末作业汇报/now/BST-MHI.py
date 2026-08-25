import cv2
import numpy as np

# 初始化参数
frame_width = 640
frame_height = 480
reference_frame = None
accumulated_frame = None
motion_history = None
mhi_duration = 2000  # MHI的持续时间（以毫秒为单位）
timestamp = 0  # 时间戳

# 创建VideoCapture对象
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

while True:
    # 读取当前帧
    ret, frame = capture.read()

    if not ret:
        break

    # 将当前帧转换为灰度图像
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 初始化运动历史图像（MHI）
    if reference_frame is None:
        reference_frame = gray_frame
        accumulated_frame = np.zeros_like(gray_frame, dtype=np.float32)
        motion_history = np.zeros_like(gray_frame, dtype=np.float32)

    # 计算当前帧与参考帧的差异
    frame_diff = cv2.absdiff(reference_frame, gray_frame)

    # 应用阈值处理
    _, threshold = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)

    # 更新累积帧
    cv2.accumulateWeighted(frame_diff, accumulated_frame, 0.5)

    # 更新运动历史图像（MHI）
    timestamp = cv2.getTickCount() / cv2.getTickFrequency() * 1000  # 获取当前时间戳
    cv2.motempl.updateMotionHistory(threshold, motion_history, timestamp, mhi_duration)

    # 显示结果
    cv2.imshow("Motion History Image", motion_history.astype(np.uint8))

    # 按下ESC键退出循环
    if cv2.waitKey(1) == 27:
        break

# 释放资源
capture.release()
cv2.destroyAllWindows()