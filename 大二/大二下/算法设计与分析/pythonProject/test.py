import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 创建动画帧
def animate(frame):
    plt.cla()
    # 绘制所有的点
    for point in arr:
        plt.scatter(point.x, point.y, color='blue')
    # 绘制已经经过的路径
    curr_points = path[:frame+1]
    for i in range(len(curr_points)):
        if i > 0:
            plt.plot([curr_points[i-1].x, curr_points[i].x], [curr_points[i-1].y, curr_points[i].y], color='blue')
    # 突出显示当前点
    plt.scatter(curr_points[-1].x, curr_points[-1].y, color='red', zorder=10)
    plt.title('Frame {}'.format(frame + 1))
    plt.xlim(0, 10)
    plt.ylim(0, 10)

# 创建动画
def create_animation():
    fig = plt.figure(figsize=(8, 6))
    ani = animation.FuncAnimation(fig, animate, frames=len(path), interval=500, repeat=False)
    ani.save('animation_test.gif', writer='pillow', fps=2)  # 保存为GIF文件

# 示例数据
arr = [Point(1, 2), Point(3, 6), Point(9, 4), Point(3, 7), Point(5, 10),
       Point(2, 3), Point(4, 5), Point(7, 6), Point(8, 8), Point(9, 8)]

path = [Point(1,2),Point(2,3),Point(1,2),Point(2,3),Point(3, 7),Point(4, 5),Point(4, 5),
        Point(3, 6),Point(3, 6),Point(3, 7),Point(5, 10),Point(7, 6),Point(8, 8),Point(5, 10),
        Point(8, 8),Point(7, 6),Point(5, 10),Point(7, 6),Point(9, 4),Point(9, 8),Point(7, 6),
        Point(8, 8),Point(7, 6),Point(9, 4),Point(7, 6),Point(9, 8),Point(8, 8),Point(9, 4),Point(8, 8),Point(9, 8)]

# 创建并保存动画
create_animation()