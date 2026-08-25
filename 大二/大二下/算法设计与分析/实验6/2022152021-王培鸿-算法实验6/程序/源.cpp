#include <stdio.h>
#include <queue>
#include <string.h>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <sstream>
#include <chrono>
#include <vector>
#include <random>
#define N 1000
using namespace std;
string file[11] = { "teams4.txt", "teams4a.txt","teams5.txt","teams7.txt","teams24.txt","teams32.txt","teams36.txt","teams42.txt","teams48.txt","teams54.txt" ,"teams60.txt" };
int n, **e, inf = 0x7f7f7f;
vector<int>flow;
vector<int>pre;
vector<bool>visit;
int m;	//	队伍数目
int bfs(int s, int t)
{
	// 初始化visit数组
	// memset(pre, -1, sizeof(pre));
	visit.resize(N);
	std::fill(pre.begin(), pre.end(), -1);
	std::fill(visit.begin(), visit.end(), false);
	queue<int>q;
	q.push(s);
	visit[s] = true;
	flow[s] = inf;                       //最开始流量为无穷 
	while (!q.empty())
	{
		int u = q.front();
		q.pop();
		if (u == t)
		{
			int minflow = flow[t];
			for (int j = t; pre[j] != -1; j = pre[j])
			{
				e[pre[j]][j] -= minflow;
				e[j][pre[j]] += minflow;
			}
			return minflow;
		}
		// 

		for (int v = 1; v <= n; v++)         //求増广路 
		{
			if (e[u][v] > 0 && !visit[v])   //注意v!=s 
			{
				pre[v] = u;
				visit[v] = true;
				q.push(v);
				flow[v] = min(flow[u], e[u][v]);         //现在的流量是流过来的流量和可以流走的量的最小值 
			}
		}
	}
	return 0;
	//if (pre[t] == -1)                   //如果没有到达终点 
	//	return -1;
	//return flow[t];                      //返回流量 
}

int EK(int s, int t)
{
	// 最大流
	int ans = 0;
	while (1)
	{
		int d = bfs(s, t);
		if (d == 0)                    //无法在找増广路 
			break;
		// 最大流加上当前流
		ans += d;
	}
	return ans;
}


// Dinic 算法
int level[N]; // 层次
int ptr[N]; // 当前弧指针
bool bfs() {
	// memset(level, -1, sizeof(level));
	for (int i = 0; i <= n; i++)
		level[i] = -1;
	queue<int> q;
	q.push(1);
	level[1] = 0;
	//flow[1] = inf;
	while (!q.empty()) {
		int u = q.front();
		q.pop();
		for (int v = 1; v <= n; v++) {
			if (level[v] == -1 && e[u][v] > 0) {
				level[v] = level[u] + 1;
				//flow[v] = min(flow[u], e[u][v]);
				//
				if (v == n)
					return true;
				q.push(v);
			}
		}
	}
	return false;
	//return level[n] != -1;
}

int dfs(int u, int flow) {
	if (u == n || flow == 0)	return flow;
	int f = 0;
	for (int i=1; i <= n; i++)
	{
		// 邻接关系
		if (level[i] == level[u] + 1 && e[u][i] > 0)
		{
			int df = dfs(i, min(flow, e[u][i]));
			if (df > 0)
			{
				e[u][i] -= df;
				e[i][u] += df;
				f += df;
				flow -= df;
				if (flow == 0)
					break;
			}
		}
	}
	return f;
}

int dinic() {
	int max_flow = 0;
	while (bfs()) {
		int flow = dfs(1, inf);
		if (flow == 0)
			break;
		max_flow += flow;
	}
	return max_flow;
}

int main()
{
	string* team = new string[N];

	int win[N], lose[N], r[N];
	int** g = new int* [N];
	e = new int* [N];
	for (int i = 0; i < N; i++)
	{
		g[i] = new int[N];
		e[i] = new int[N];
	}
	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < N; j++)
		{
			g[i][j] = 0;
			e[i][j] = 0;
		}
	}

	// memset(g, 0, sizeof(g));
	flow.resize(N), pre.resize(N);

	string path = "D:\\作业\\算法设计与分析\\实验6\\baseball\\"+file[0];
	//string path = "D:\\作业\\算法设计与分析\\实验6\\baseball\\data\\" + to_string(100) + ".txt";
	// 打开文件
	ifstream file(path);
	if (!file.is_open())
	{
		std::cerr << "文件打开失败" << endl;
		return 1;
	}
	else
	{
		std::cout << "成功打开文件：" << path << endl;
	}
	string line;
	getline(file, line);
	istringstream iss(line);
	iss >> m;
	// 邻接矩阵的大小
	n = (m - 1) * (m - 2) / 2 + (m - 1) + 2;

	int i = 0;
	// 读取边集
	while (std::getline(file, line)) {
		std::istringstream iss(line);
		string str;
		int w, l, tr;
		iss >> str;
		iss >> w; iss >> l; iss >> tr;
		// 更新数组
		team[i] = str;
		win[i] = w;
		lose[i] = l;
		r[i] = tr;
		int t;
		// 输入g[i][j]矩阵
		for (int j = 0; j < m; j++)
		{
			iss >> t;
			g[i][j] = t;
		}
		i++;
	}
	
	// 执行算法
	auto start = chrono::steady_clock::now();
	// 最大流算法处理
	for (int i = 0; i < m; i++)
	{
		int s = win[i] + r[i];
		// cout << s << endl;
		// 寻找最少胜场的队伍
		int mw = 0;
		for (int j = 0; j < m; j++)
		{
			if (j != i)
			{
				if (mw < win[j])
					mw = win[j];
			}
		}
		// cout << s << " " << mw << endl;
		// 不是平凡淘汰
		if (s >= mw)
		{
			// memset(e, 0, sizeof(e));
			for (int j = 0; j <= n; j++)
				for (int k = 0; k <= n; k++)
					e[j][k] = 0;

			// r[i][j]之和
			int sum = 0;
			// 迁移图表
			int tu[N][N], row = 0, col = 0;
			for (int j = 0; j < m; j++)
			{
				if (j != i)
				{
					for (int k = 0; k < m; k++)
					{
						if (k != i)
						{
							tu[row][col++] = g[j][k];
						}
					}
					row++;
					col = 0;
					// col++;
				}
			}
			// 比赛点的添加
			int t = (m - 1) * (m - 2) / 2;
			int c = 1;
			for (int j = 0; j < m - 1; j++)
			{

				for (int k = j+1; k < m-1; k++)
				{
					// 比赛点
					e[1][1 + c] = tu[j][k];
					sum += tu[j][k];
					// 比赛点到队伍点
					e[1 + c][t + 2 + j] = inf;
					e[1 + c][t + 2 + k] = inf;
					c++;
				}
			}


			//	队伍点都T的添加
			int ji = 0;
			for (int j = 0; j < m; j++)
			{
				if (j != i)
				{
					e[t + 2 + ji][n] = s - win[j];
					ji++;
				}
			}
			// EK算法
			int f = EK(1, n);
			//int f = dinic();
			//cout << sum << " " << f << " ";
			if (sum > f)
				cout << team[i] << "非平凡淘汰" << endl;
			// printf("%d\n", EK(1, n)); 
		}
	}
	// 输出算法执行时间
	auto end = chrono::steady_clock::now();
	auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
	std::cout << duration.count() << "ms\n";
	// printf("%d\n", EK(1, n)); 
	

	/*
	n = 900;
	// 随机样例测试
	// 读取边集
	for (int i = 1; i <= n; i++)
	{
		for (int j = i + 1; j <= n; j++)
		{
			//设置随机数种子
			std::random_device rd;
			std::mt19937 gen(rd());
			std::uniform_int_distribution<> dis(0, 100);
			// srand((unsigned)time(NULL));
			int f = dis(gen);
			e[i][j] += f;
		}
	}
	// 测试算法时间
	// 执行算法
	cout << "点个数为：" << n << endl;
	auto start = chrono::steady_clock::now();
	//int f = EK(1, n);
	//cout << f << endl;
	dinic();
	// 输出算法执行时间
	auto end = chrono::steady_clock::now();
	auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
	std::cout << duration.count() << "ms\n";
	*/

	
	return 0;
}