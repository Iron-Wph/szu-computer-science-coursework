#include <iostream>
#include <vector>
#include <sstream>
#include <fstream>
#include <string>
#include <chrono>
using namespace std;
int m = 15;              // 总共可选的颜色数目
int points = 450;       // 顶点的个数
class point
{
public:
    // 顶点的颜色，从0到m-1枚举
    int color;
    int *state = new int[m];         // 顶点的颜色状态
    int choice = 0;                  // 顶点的颜色选择个数
    int *adj = new int[points+1];    // 与该点相邻的点
    int degree;
    point()
    {
        // 初始化邻接表
        for(int i=0;i<points+1;i++)
            adj[i] = 0;
        // 没填颜色
        color = -1;
        // 初始化为1，代表颜色可填
        for(int i=0;i<m;i++)
            state[i] = 1;
        choice = m;
    }
};
point tu[451];      // 图的邻接表
int sum = 0;            // 记录填充方案的个数

// 向前探测函数
bool forward_check(int j)
{
    // 遍历与该点邻接的点
    for(int i=1;i<=tu[j].adj[0];i++)
    {
        // 如果邻接点没有填颜色且没有颜色可以填
        if(tu[tu[j].adj[i]].color == -1 && tu[tu[j].adj[i]].choice == 0)
        {   
            return false;
        }
    }
    return true;
}

bool bound(int j)
{
	bool flag = true;
	// 遍历与该点邻接的点
    for(int i=1;i<=tu[j].adj[0];i++)
    {
        if(tu[tu[j].adj[i]].color == tu[j].color)
        {
            flag = false;
            return flag;
        }
    }
    return flag;
}

int MRV_DH()
{
    // 选择最小可选颜色数目的点
    int min_color = 9999;
    int max_degree = 0;
    int index = 1;
    // 
    for(int i=1;i<=points;i++)
    {
        // 如果该点没有填颜色
        if(tu[i].color == -1)
        {
            if(tu[i].choice < min_color)
            {
                min_color = tu[i].choice;
                index = i;
                max_degree = tu[i].degree;
            }
            // 如果该点的度更大，则选为起点
            else
            {
                if(min_color ==  tu[i].choice && tu[i].degree > max_degree)
                {
                    max_degree = tu[i].degree;
                    index = i;
                }
            }
        }
    }
    //cout<<index<<endl;
    return index;
}
clock_t startTime,endTime;
int select = 0;
//核心的回溯函数
int color(int current, int count, int usedColor) { //count是已经着色的点的数量
	if (count == points) { //到达叶子节点,找到一个着色方案
		sum += tu[current].choice;
		return tu[current].choice;
	}
	else {
		int s = 0;
		for (int i = 0; i < m; i++) {
			if (tu[current].state[i] == 1) 
            {
				int ss = 0;
				tu[current].color = i;
				auto isNewColor = i > usedColor;
				//剪枝

                    int *change = new int[points];      // 保存由于当前结点影响的其他结点
                    int tk = 0;
                    // 更新相邻结点的信息
                    for(int k=1;k<=tu[current].adj[0];k++)
                    {   
                        if(tu[tu[current].adj[k]].color == -1)
                        {
                            // 
                            tu[tu[current].adj[k]].degree--;
                            // 当前颜色本来可选
                            if(tu[tu[current].adj[k]].state[i]==1)
                            {
                                // 保存被修改的点
                                change[tk++] = tu[current].adj[k];
                                tu[tu[current].adj[k]].state[i] = 0;
                                tu[tu[current].adj[k]].choice--;
                            }
                        }
                    }
                    if(forward_check(current))
                    {
                        // 当前结点的信息更新
                        tu[current].state[i] = 0;
                        tu[current].choice--;
                        // 递归
					    if (isNewColor)
						    ss = color(MRV_DH(), count + 1, usedColor + 1);
					    else
						    ss = color(MRV_DH(), count + 1, usedColor);
                        // 
                        tu[current].state[i] = 1;
                        tu[current].choice++;
                    }
                    // 回溯其他点的状态
                    for(int j=1;j<=tu[current].adj[0];j++)
                    {
                        if(tu[tu[current].adj[j]].color == -1)
                        {
                            tu[tu[current].adj[j]].degree++;
                        }
                    }
                    for(int j = 0;j < tk; j++)
                    {   
                        // 恢复其他点的状态
                        tu[change[j]].state[i] = 1;
                        tu[change[j]].choice++;
                    }
                    delete []change;
				
                tu[current].color = -1;
				//关键剪枝
				if (isNewColor) {
					s += ss * (m - usedColor-1);
					sum += ss * (m - usedColor);
					break;
				}
				s += ss;
			}
		}
		if (sum > 1e8) 
		{
			endTime = clock();
			cout<<"sum:"<<sum<<endl;
			cout << (double)(endTime - startTime) << "ms" << endl;
			exit(1);
		}
		else
		{
			return s;
		}
	}
}



int main()
{
    // 读取的文件
    points = 100;	
    // string path = "D:\\color\\random_seed\\p100 e1900.txt";
    
	string path = "D:\\作业\\算法设计与分析\\实验3\\data\\le450_5a.txt";
    //string path = "D:\\作业\\算法设计与分析\\实验3\\test.txt";
    ifstream file(path);
    if(!file.is_open())
    {
        std::cout<<"文件打开失败！\n";
        return 0;
    }
    else
    {
        std::cout<<path<<"文件打开成功！\n";
    }
    // 读取文件
    string line;
    char e;
    int a,b;
    while(getline(file,line))
    {
        // 读取一行
        istringstream is(line);
        is>>e>>a>>b;
        // 压入邻接表
        int la = tu[a].adj[0];
        int lb = tu[b].adj[0];
        tu[a].adj[la+1] = b;
        tu[b].adj[lb+1] = a;
        tu[a].adj[0]++;
        tu[b].adj[0]++;
    }
    
    //
    for(int j=0;j<=points;j++)
    {
        tu[j].degree = tu[j].adj[0];
    }
    // 排序并计时
    startTime = clock();
    color(1, 1, -1);
	endTime = clock();
	cout<<"sum:"<<sum<<endl;
	cout<<(double)(endTime - startTime)<<"ms\n";
//    auto start = chrono::steady_clock::now();
//    
//    int td = color(1, 1, -1);
//
//    auto end = chrono::steady_clock::now();
//    auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
//
//	std::cout<<"sum:"<<td<<endl;
//    std::cout<<"time:"<<duration.count()<<"ms"<<endl;

    system("pause");
    return 0;
}