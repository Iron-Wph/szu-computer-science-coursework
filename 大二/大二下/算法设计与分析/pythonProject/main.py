import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def distance(arr):
    n = len(arr)
    min_dist = math.inf
    closest_pair = None

    fig, ax = plt.subplots()
    points, = ax.plot([], [], 'bo')
    current_line, = ax.plot([], [], 'g--', linewidth=2)  # 当前遍历的边
    shortest_line, = ax.plot([], [], 'r-', linewidth=2)  # 最短边

    def init():
        ax.set_xlim(0, 15)
        ax.set_ylim(0, 15)
        ax.set_xlabel('X轴')
        ax.set_ylabel('Y轴')
        ax.set_title('暴力法求解过程')
        return points, current_line, shortest_line

    def update(frame):
        nonlocal min_dist
        nonlocal closest_pair

        if frame >= n * (n - 1) // 2 - 1:
            return points, current_line, shortest_line

        i = frame // (n - 1)
        j = frame % (n - 1)
        if j >= i:
            j += 1

        pa = arr[i]
        pb = arr[j]
        dist = math.sqrt((pa.x - pb.x) ** 2 + (pa.y - pb.y) ** 2)

        if dist < min_dist:
            min_dist = dist
            closest_pair = (pa, pb)

        current_line.set_data([pa.x, pb.x], [pa.y, pb.y])
        shortest_line.set_data([closest_pair[0].x, closest_pair[1].x], [closest_pair[0].y, closest_pair[1].y])
        points.set_data([p.x for p in arr], [p.y for p in arr])
        return points, current_line, shortest_line

    ani = animation.FuncAnimation(fig, update, frames=n * (n - 1) // 2, init_func=init, blit=True)

    return ani

# 示例数据
arr = [Point(1, 2), Point(3, 6), Point(9, 4), Point(3, 7), Point(5, 10),
       Point(2, 3), Point(4, 5), Point(7, 6), Point(8, 8), Point(9, 8)]

# 生成动画对象
ani = distance(arr)

# 保存为gif动图
ani.save('animation.gif', writer='pillow')