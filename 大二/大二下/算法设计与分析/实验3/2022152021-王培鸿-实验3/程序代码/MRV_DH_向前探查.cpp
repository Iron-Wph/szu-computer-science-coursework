#include <iostream>
#include <vector>
#include <sstream>
#include <fstream>
#include <string>
#include <chrono>
using namespace std;
int m = 4;              // 总共可选的颜色数目
int points = 9;       // 顶点的个数
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
point tu[1001];      // 图的邻接表
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
    return index;
}
clock_t startTime, endTime;//秒级程序计时
int select = 0;
void color(int t)
{
    if(sum == 1e8)
        return;
	if(select>=points)	
	{
		sum++;
        //cout<<sum<<endl;
//        endTime = clock();
//		cout<<"sum:"<<sum<<endl;
//		cout<<(double)(endTime - startTime)<<"ms\n";
//		exit(1);
		return;
	}
	else
	{	
		//	m代表总共的颜色数目
		for(int i=0;i<m;i++){
			// 尝试填充某种颜色
			tu[t].color = i;
			// 如果填充合法就进入下一个顶点
			if(bound(t))
            {
                int *change = new int[points];      // 保存由于当前结点影响的其他结点
                int tk = 0;
                // 更新相邻结点的信息
                for(int k=1;k<=tu[t].adj[0];k++)
                {   
                    if(tu[tu[t].adj[k]].color == -1)
                    {
                        // 
                        tu[tu[t].adj[k]].degree--;
                        // 当前颜色本来可选
                        if(tu[tu[t].adj[k]].state[i]==1)
                        {
                            // 保存被修改的点
                            change[tk++] = tu[t].adj[k];
                            tu[tu[t].adj[k]].state[i] = 0;
                            tu[tu[t].adj[k]].choice--;
                        }
                    }
                }

                if(forward_check(t))
                {
                    // 当前结点的信息更新
                    tu[t].state[i] = 0;
                    tu[t].choice--;
                    select++;
                    //
                    color(MRV_DH());
                    // 如果填充不合法，回溯
                    select--;
                    tu[t].state[i] = 1;
                    tu[t].choice++;
                }

                // 回溯其他点的状态
                for(int j=1;j<=tu[t].adj[0];j++)
                {
                    if(tu[tu[t].adj[j]].color == -1)
                    {
                        tu[tu[t].adj[j]].degree++;
                    }
                }
                for(int j = 0;j < tk; j++)
                {   
                    // 恢复其他点的状态
                    tu[change[j]].state[i] = 1;
                    tu[change[j]].choice++;
                }
                delete []change;
            }
            // 回溯状态
            tu[t].color = -1;
		}
	}
}

int main()
{
    // 读取的文件
    //points = 700;
	//string path = "D:\\color\\random_seed\\p700 e10500_3.txt";
    //string path = "D:\\作业\\算法设计与分析\\实验3\\data\\le450_"+to_string(m)+"a.txt";
    string path = "D:\\作业\\算法设计与分析\\实验3\\test.txt";
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
    color(1);
	endTime = clock();
	cout<<"sum:"<<sum<<endl;
	cout<<(double)(endTime - startTime)<<"ms\n";
//    auto start = chrono::steady_clock::now();
//    
//    color(1);
//    auto end = chrono::steady_clock::now();
//    auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
//
//	std::cout<<"sum:"<<sum<<endl;
//    std::cout<<"time:"<<duration.count()<<"ms"<<endl;

    system("pause");
    return 0;
}