import numpy as np
 # 独⽴实现IoU计算函数
def compute_iou(box1, box2):
    """计算两个边界框的交并⽐（框格式：[xmin, ymin, xmax, ymax]）"""
    xmin1, ymin1, xmax1, ymax1 = box1
    xmin2, ymin2, xmax2, ymax2 = box2
    
    # 交集坐标
    inter_xmin = max(xmin1, xmin2)
    inter_ymin = max(ymin1, ymin2)
    inter_xmax = min(xmax1, xmax2)
    inter_ymax = min(ymax1, ymax2)
    
    # 交集⾯积
    inter_area = max(0, inter_xmax - inter_xmin) * max(0, inter_ymax - inter_ymin)

    # 两个框的并集面积
    union_area = (xmax1 - xmin1) * (ymax1 - ymin1) + (xmax2 - xmin2) * (ymax2 - ymin2) - inter_area

    # 计算IoU
    iou = inter_area / union_area if union_area != 0 else 0
    return iou

 # 独⽴实现锚框⽣成函数
def create_anchors(base_sizes=[16, 32, 64], aspect_ratios=[0.5, 1, 2]):
    """
    ⽣成不同尺⼨和宽⾼⽐的锚框
        base_sizes: 基准尺⼨列表（锚框的参考⼤⼩）
        aspect_ratios: 宽⾼⽐（w/h）列表
    返回：锚框列表（格式：[w, h]）
    """
    anchors = []
    for base in base_sizes:
        for ratio in aspect_ratios:
        # 计算宽⾼（保持⾯积≈base²）
        # 宽⾼⽐ ratio = w/h → w = ratio * h
        # ⾯积 w*h = ratio * h² ≈ base² → h = base / sqrt(ratio)
            h = base / np.sqrt(ratio)
            w = base * np.sqrt(ratio)
            anchors.append([round(w, 1), round(h, 1)])  # 保留1位⼩数
    
    return anchors

# 主程序：⽣成锚框并计算与⽬标的IoU
if __name__ == "__main__":
    # 定义基准参数
    # base_sizes = [16, 32, 64]    
    base_sizes = [15, 25, 35]    
    # 基准尺⼨
    # aspect_ratios = [0.5, 1, 2]  # 宽⾼⽐（w/h）
    aspect_ratios = [0.7, 1, 1.5]  # 宽⾼⽐（w/h）
    
    # ⽣成锚框
    anchors = create_anchors(base_sizes, aspect_ratios)
    print(f"基准尺⼨：{base_sizes}，宽⾼⽐：{aspect_ratios}")
    print(f"⽣成的锚框（宽, ⾼）：{anchors}")
    # 定义⽬标框（假设宽30，⾼30）
    target_wh = [30, 30]  # [w, h]
    print(f"\n⽬标框（宽, ⾼）：{target_wh}")
    # 转换为边界框格式（中⼼在原点，便于计算IoU）
    def wh_to_bbox(wh):
        w, h = wh
        return [-w/2, -h/2, w/2, h/2]  # [xmin, ymin, xmax, ymax]
    target_bbox = wh_to_bbox(target_wh)
    
    # 计算每个锚框与⽬标的IoU
    iou_scores = []
    for anchor in anchors:
        anchor_bbox = wh_to_bbox(anchor)
        iou_val = compute_iou(target_bbox, anchor_bbox)
        iou_scores.append(round(iou_val, 3))
    
    # 输出结果
    print("\n锚框与⽬标的IoU：")
    for i, (anchor, iou_val) in enumerate(zip(anchors, iou_scores)):
        print(f"锚框{i+1}（宽={anchor[0]}, ⾼={anchor[1]}）：IoU={iou_val}")
    
    # 找到最佳匹配锚框
    best_idx = np.argmax(iou_scores)
    print(f"\n最佳匹配锚框：{anchors[best_idx]}，IoU={iou_scores[best_idx]}")
    print("说明：锚框尺⼨和⽐例越接近⽬标，IoU越⾼")