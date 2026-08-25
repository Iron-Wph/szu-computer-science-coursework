import cv2
import matplotlib.pyplot as plt

# 读取图像
image = cv2.imread("57.jpg")
# 改变大小
image = cv2.resize(image, (800, 600))

# 进行双边滤波
filtered_image = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)

# 进行高斯滤波
# filtered_image_Gauss = cv2.GaussianBlur(image, (9, 9), sigmaX=2, sigmaY=2)
# cv2.imshow("Gauss",filtered_image_Gauss)


# 显示原始图像和滤波后的图像
cv2.imshow("Original Image", image)
cv2.imshow("Filtered Image", filtered_image)



# 将图像从RGB颜色空间转换为YCrCb颜色空间
ycrcb_image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

# 提取Cr通道
cr_channel = ycrcb_image[:, :, 1]
# 提取Cb通道
cb_channel = ycrcb_image[:, :, 2]


# 使用Otsu阈值法进行二值化
_, cr_binary_image = cv2.threshold(cr_channel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
_, cb_binary_image = cv2.threshold(cb_channel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 显示原始图像、Cr通道直方图和二值化图像
cv2.imshow("Cr Channel Histogram", cv2.resize(cr_channel, None, fx=0.5, fy=0.5))
cv2.imshow("cr Binary Image", cr_binary_image)
cv2.imshow("cb Binary Image", cb_binary_image)
# # 保存文件
# cv2.imwrite("67_image.jpg", image)
# cv2.imwrite("67_filtered_image.jpg", filtered_image)
# cv2.imwrite("67_cr.jpg", cr_binary_image)
# cv2.imwrite("67_cb.jpg", cb_binary_image)


# 绘制cr, cb通道的灰度直方图

# 计算灰度直方图
cr_histogram = cv2.calcHist([cr_channel], [0], None, [256], [0, 256])
cb_histogram = cv2.calcHist([cb_channel], [0], None, [256], [0, 256])

# # 绘制灰度直方图
# plt.plot(cr_histogram, color='gray')
# plt.xlabel('Pixel Value')
# plt.ylabel('Frequency')
# plt.title('Cr Channel Histogram')
# # save image file
# plt.savefig("cr_histogram.png")
# plt.show()
#
# plt.plot(cb_histogram, color='gray')
# plt.xlabel('Pixel Value')
# plt.ylabel('Frequency')
# plt.title('Cb Channel Histogram')
# # save image file
# plt.savefig("cb_histogram.png")
# plt.show()
#
# # 关闭图像窗口
# plt.close()



# 定义图像的宽度和高度
image_width = cb_binary_image.shape[1]
image_height = cb_binary_image.shape[0]

# 定义四个顶点的位置
v1 = [0, 0]
v2 = [image_width - 1, 0]
v3 = [0, image_height - 1]
v4 = [image_width - 1, image_height - 1]

# 定义直线的斜率和截距
slope_v1v4 = -1
slope_v2v3 = 1
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

# 显示键盘定位结果
cv2.imshow("Keyboard Localization", result_image)




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
print(bounding_boxes)
print(key_centers)
# 显示结果图像
cv2.imshow("Result", cb_binary_image)

cv2.waitKey(0)
cv2.destroyAllWindows()