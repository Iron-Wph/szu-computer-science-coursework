import numpy as np
import random
from PIL import Image
random.seed(0)


def gen_yzm(char_info='8CG4'):

    # 设置斑点
    bd = np.ones((2, 2, 3), dtype='uint8')
    bd[:, :, 0] = 250  # R通道
    bd[:, :, 1] = 0  # G通道  
    bd[:, :, 2] = 0    # B通道

    # 设置白色底图
    sz = (30, 93, 3)  # 图像大小
    bg = np.ones(shape=sz, dtype='uint8') * 225  #白色

    # 设置随机斑点位置
    num = 35
    for _ in range(num):
        r = random.randint(0, sz[0] - 2)  # 行
        c = random.randint(0, sz[1] - 2)  # 列
        bg[r: r + 2, c: c + 2, :] = bd   # 填充斑点

    # Image.fromarray(bg).show()

    # 设置字符列表:大写字母、小写字母、数字
    cns = [chr(c) for c in list(range(97, 97 + 26)) + list(range(65, 65 + 26)) + list(range(48, 48 + 10))]

    # 对应到字符模板库
    int_info = [cns.index(c) for c in char_info]

    # 起始列位置
    x_s = 4
    # 颜色库
    colors = [
        [0, 0, 255],
        [58, 95, 205],
        [105, 89, 205],
        [131, 111, 255],
        [0, 0, 139],
        [16, 78, 139],
        [54, 100, 139],
    ]

    for i in int_info:
        # 读取字符模板
        im_path = f'验证码数据集/db/{i:02d}.jpg'
        img = np.array(Image.open(im_path).convert('1'))

        # 随机提取颜色库的颜色
        co = random.choice(colors)

        # 设置r颜色通道
        imi_r = np.ones(img.shape) * 255
        imi_r[img] = co[0]

        # 设置g颜色通道
        imi_g = np.ones(img.shape) * 255
        imi_g[img] = co[1]

        # 设置b颜色通道
        imi_b = np.ones(img.shape) * 255
        imi_b[img] = co[2]

        # 合并RGB三通道
        imi = np.concatenate([np.expand_dims(imi_r, -1), np.expand_dims(imi_g, -1), np.expand_dims(imi_b, -1)], 2)

        # 设置纵向的位置
        r_si = random.randint(4, sz[0] - img.shape[0] - 2)
        c_si = x_s

        # 字符图像填充到底图
        bg[r_si: r_si + img.shape[0], c_si: c_si + img.shape[1], :][img] = imi[img]

        # 更新起始列，中间设置隔10列
        x_s = c_si + img.shape[1] + 10

    # 转换为图像
    Image.fromarray(bg).show()
    return Image.fromarray(bg)


if __name__ == '__main__':
    gen_yzm()