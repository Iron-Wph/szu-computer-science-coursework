import numpy as np

def iou(box1, box2):
    """
    计算两个边界框的交并⽐(IoU)
        box1: 边界框1，格式[xmin, ymin, xmax, ymax]
        box2: 边界框2，格式[xmin, ymin, xmax, ymax]
    返回: IoU值（0-1之间）
    """
    # 计算交集区域坐标
    xmin1, ymin1, xmax1, ymax1 = box1
    xmin2, ymin2, xmax2, ymax2 = box2
    
    inter_xmin = max(xmin1, xmin2)
    inter_ymin = max(ymin1, ymin2)
    inter_xmax = min(xmax1, xmax2)
    inter_ymax = min(ymax1, ymax2)
    
    # 计算交集面积，无交集面积则为0
    inter_width = max(0, inter_xmax - inter_xmin)
    inter_height = max(0, inter_ymax - inter_ymin)
    inter_area = inter_width * inter_height
    
    # 计算两个box的面积
    area1 = (xmax1 - xmin1) * (ymax1 - ymin1)
    area2 = (xmax2 - xmin2) * (ymax2 - ymin2)
    
    # 计算并集面积
    union_area = area1 + area2 - inter_area

    # IOU：交集面积 / 两个框的并集面积
    return inter_area / union_area if union_area != 0 else 0

def nms(boxes, scores, iou_threshold):
    """
    ⾮极⼤值抑制(NMS)：过滤重叠度⾼的边界框
        boxes: 边界框列表，格式[[xmin, ymin, xmax, ymax], ...]
        scores: 每个边界框的置信度列表
        iou_threshold: IoU阈值，超过该值的框会被过滤
    返回: 保留的边界框索引
    """
    # 如果没有边界框，返回空列表
    if len(boxes) == 0:
        return []
    
    # 将边界框转换为numpy数组方便处理
    boxes = np.array(boxes)

    # 提取每个框的坐标
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    # 按置信度降序排序，获取排序索引
    # 切片是[start:end:step]，-1表示从末尾到开头
    order = np.argsort(scores)[::-1]
    keep = []  # 用于存储保留的边界框索引
    while len(order)>0:
        # 取出置信度最高的框索引
        top_idx = order[0]
        keep.append(top_idx)
        
        # 计算当前框与其他框的IoU
        ious = np.array([iou(boxes[top_idx], boxes[i]) for i in order[1:]])
        # 保留IoU小于阈值的框
        # 找到所有IoU小于等于阈值的索引
        mask = ious <= iou_threshold
        # 保留对应的框索引
        order = order[1:][mask]
    
    return keep

if __name__ == "__main__":
    boxes = [
        [50, 60, 150, 180],  # 框1
        [55, 65, 145, 175],   # 框2（与框1⾼度重叠）
        [200, 210, 300, 320], # 框3
        [205, 215, 295, 315]  # 框4（与框3⾼度重叠）
    ]
    
    scores = [0.9, 0.85, 0.92, 0.88]  # 每个框的置信度
    threshold = 0.7  # NMS的IoU阈值
    keep_indices = nms(boxes, scores, iou_threshold=threshold)
    keep_boxes = [boxes[i] for i in keep_indices]
    
    print("原始边界框：", boxes)
    print("原始置信度：", scores)
    print(f"NMS阈值{threshold}时保留的边界框索引：{keep_indices}")
    print(f"保留的边界框：{keep_boxes}")

        