import cv2
import os
import numpy as np
from PIL import Image
from tqdm import tqdm
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def char_segment(image, show=False):
    if isinstance(image, str):
        # 读取bgr图像
        image_bgr = cv2.imread(image)
    elif isinstance(image, Image.Image):
        # PIL图像转bgr
        image_bgr = np.array(image, dtype='uint8')[:, :, ::-1]
    elif isinstance(image, np.ndarray):
        image_bgr = image.copy()

    # 将rgb图像转为灰度图
    image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    # 对灰度图进行均值滤波
    image_gray = cv2.blur(image_gray, (2, 2))

    # 二值化
    _, image_bin = cv2.threshold(image_gray, int(255 * 0.8), 255, cv2.THRESH_BINARY_INV)


    # 对图像进行连通域分析
    _, _, stats, _ = cv2.connectedComponentsWithStats(image_bin, connectivity=4)

    stats = list(stats)
    # 按照面积进行排序
    stats.sort(key=lambda x: x[-1])

    boxes = []
    # 遍历连通域检测结果
    for s in stats:
        x, y, w, h, area = s
        # 过滤掉表面积小的连通域
        if area < 30 or area > 1000:
            continue
        # 保存外接矩形
        boxes.append([x, y, w, h])
        # 分割完成
        if len(boxes) == 4:
            break

    # 从左向右排序
    boxes = sorted(boxes, key=lambda x: x[0])

    crops = []
    # 遍历外接矩形框
    for box in boxes:
        x, y, w, h = box
        # 裁剪图像
        crop = image_bgr[y: y + h, x: x + w, :]
        crops.append(crop)

        if show:
            # 绘制连通域外接矩形
            cv2.rectangle(image_bgr, (x, y), (x + w, y + h), (0, 0, 255), 1)

    if show:
        cv2.imshow('result', image_bgr)
        cv2.waitKey()

    return crops, boxes, image_bgr.copy()


def char_segment2(image):
    if isinstance(image, str):
        # 读取bgr图像
        image_bgr = cv2.imread(image)
    elif isinstance(image, Image.Image):
        # PIL图像转bgr
        image_bgr = np.array(image, dtype='uint8')[:, :, ::-1]
    elif isinstance(image, np.ndarray):
        image_bgr = image.copy()

    # 将rgb图像转为灰度图
    image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    szs = np.linspace(2, 94, 5)

    ims = []
    for i in range(len(szs) - 1):
        i = int(i)
        ims.append(cv2.cvtColor(image_gray[:, int(szs[i])-2: int(szs[i + 1])+2], cv2.COLOR_GRAY2BGR))

    return ims, None, image_bgr.copy()


if __name__ == '__main__':
    # 创建分割字符数据库
    dbc = '验证码数据集/dbc'
    if not os.path.exists(dbc):
        try:
            os.mkdir(dbc)
            logging.info(f"成功创建目录: {dbc}")
        except Exception as e:
            logging.error(f"创建目录 {dbc} 失败: {e}")
            exit(1)

    # 设置字符列表:大小写字母、数字
    cns = [chr(c) for c in list(range(97, 97 + 26)) + list(range(65, 65 + 26)) + list(range(48, 48 + 10))]
    # 排除字母o、O、l、I、i、j
    exclude_cns = 'oOlIij'
    cns = [c for c in cns if c not in exclude_cns]
    print(cns)
    # 创建类别文件夹
    for c in cns[22:]:
        class_dir = os.path.join(dbc, c)
        if not os.path.exists(class_dir):
            try:
                os.mkdir(class_dir)
                logging.info(f"成功创建类别目录: {class_dir}")
            except Exception as e:
                logging.error(f"创建类别目录 {class_dir} 失败: {e}")
                continue

    # 所有验证码
    try:
        yzms = os.listdir('验证码数据集/yzms')
        logging.info(f"找到 {len(yzms)} 个验证码文件")
    except Exception as e:
        logging.error(f"读取yzms目录失败: {e}")
        exit(1)

    # 验证yzms目录是否存在
    if not os.path.exists('验证码数据集/yzms'):
        logging.error("yzms目录不存在，请确保验证码文件存放在此目录下")
        exit(1)

    # 用于统计保存的图像数量
    saved_count = 0

    for yzm in tqdm(yzms, desc='分割验证码'):
        path = f"验证码数据集/yzms/{yzm}"
        try:
            # 对验证码进行分割
            crops, boxes, _ = char_segment(path, show=False)
            
            # 检查分割结果是否有效
            if len(crops) != 4:
                logging.warning(f"验证码 {yzm} 分割失败，只得到 {len(crops)} 个字符")
                continue
            
            # 获取验证码真实标签（假设文件名的前4个字符是验证码）
            label = yzm.split('.')[0][:4]
            
            # 遍历分割的字符并保存
            for i, (crop, char) in enumerate(zip(crops, label)):
                # 跳过不在字符列表中的字符
                if char not in cns:
                    logging.warning(f"验证码 {yzm} 中的字符 {char} 不在字符列表中，跳过保存")
                    continue
                
                # 构建保存路径
                class_dir = os.path.join(dbc, char.upper())
                file_name = f"{yzm[:-4]}_{i}.jpg"
                save_path = os.path.join(class_dir, file_name)
                
                # 保存图像
                try:
                    cv2.imwrite(save_path, crop)
                    saved_count += 1
                    # logging.info(f"成功保存字符 {char} 到 {save_path}")
                except Exception as e:
                    logging.error(f"保存字符 {char} 到 {save_path} 失败: {e}")
        
        except Exception as e:
            logging.error(f"处理验证码 {yzm} 失败: {e}")
            continue
    
    logging.info(f"分割完成，共保存 {saved_count} 个字符图像")
        
