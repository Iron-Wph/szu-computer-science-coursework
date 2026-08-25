import cv2 as cv
i = 1
while i <= 10:
    filename = f"trainset/10_Mhyang/{i}.jpg"
    image = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    # 修改图片的大小统一为：宽为120，高为90
    image = cv.resize(image, (120,90))
    cv.imshow("Image", image)
    # 移动窗口到指定位置
    window_name = "Image"
    window_x = 100  # 窗口左上角的 x 坐标
    window_y = 100  # 窗口左上角的 y 坐标
    cv.moveWindow(window_name, window_x, window_y)
    cv.waitKey(60)

    # 将修改大小后的图像存回原图
    cv.imwrite(filename, image)
    i += 1
cv.destroyAllWindows()

"""
本文件的作用是将训练样本图像的大小统一改为：宽为120，高为90的灰度图
"""