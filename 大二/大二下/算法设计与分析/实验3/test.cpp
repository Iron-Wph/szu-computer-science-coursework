#include<iostream>
#include<string.h>
#include<sstream>
#include<fstream>
#include<vector>
using namespace std;
int tu[9][9];		// 图的邻接矩阵
int colors[9];		// 存储填充的颜色
int sum = 0;			// 记录填充方案的个数
int m = 4;		// 每个点的颜色数目
int points = 9;		// 顶点的个数
bool bound(int j)
{
	bool flag = true;
	// 遍历与该点邻接的点
	for(int i=0;i < points;i++)
	{
		if(tu[i][j]!=0 && colors[j]==colors[i])
		{
			flag = false;
			return flag;
		}
	}
	return flag;
}
void color(int t)
{
	if(t>=points)	
	{
		sum++;
		return;
	}
	else
	{	
		//	m代表总共的颜色数目
		for(int i=0;i<m;i++){
			// 尝试填充某种颜色
			colors[t] = i;
			// 如果填充合法就进入下一个顶点
			if(bound(t))
			{
				color(t+1);
			}
			colors[t] = -1;
		}
	}
}
int main()
{
	// 初始化图为空图
	for(int i=0;i<points;i++)
		for(int j=0;j<points;j++)
			tu[i][j] = 0;
	for(int i=0;i<points;i++)
		colors[i] = -1;
	//
	string path = "D:\\作业\\算法设计与分析\\实验3\\test.txt";
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
		tu[a][b] = 1;
		tu[b][a] = 1;
		cout<<ch<<" "<<a+1<<" "<<b+1<<endl;
	}
	color(0);
	cout<<"sum:"<<sum<<endl;
	return 0;
}