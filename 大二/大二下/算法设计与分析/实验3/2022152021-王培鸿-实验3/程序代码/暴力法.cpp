#include<iostream>
#include<string.h>
#include<sstream>
#include<fstream>
#include<vector>
#include <chrono>
#include <ctime>
using namespace std;
int sum = 0;			// 记录填充方案的个数
int m = 5;		// 每个点的颜色数目
int points = 450;		// 顶点的个数
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
point tu[1001];		// 图的邻接矩阵
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
clock_t startTime, endTime;//秒级程序计时
void color(int t)
{
	if(t>points)	
	{
		sum++;
		endTime = clock();
		cout<<"sum:"<<sum<<endl;
		cout<<(double)(endTime - startTime)<<"ms\n";
		exit(1);
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
				color(t+1);
			}
			tu[t].color = -1;
		}
	}
}
int main()
{
	string path = "D:\\作业\\算法设计与分析\\实验3\\data\\le450_"+to_string(m)+"a.txt";
	//string path = "D:\\作业\\算法设计与分析\\实验3\\test.txt";
	ifstream file(path);
	if(!file.is_open())
	{
		cerr<<"无法打开文件"<<endl;
	}
	else
	{
		cout<<"成功打开文件"<<path<<endl;
	}
	string line;
	char ch;
	int a,b;
	while(getline(file,line))
	{
		istringstream iss(line);
		iss>>ch>>a>>b;
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
	cout<<(double)(startTime - endTime)<<"ms\n";
//    auto start = chrono::steady_clock::now();
//    
//    color(1);
//    auto end = chrono::steady_clock::now();
//    auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
//
//	cout<<"sum:"<<sum<<endl;
//    cout<<"time:"<<duration.count()<<"ms"<<endl;
	return 0;
}