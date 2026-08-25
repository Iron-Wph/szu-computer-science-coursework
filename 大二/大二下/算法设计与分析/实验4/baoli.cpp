#include <iostream>
#include <chrono>
#include <ctime>
using namespace std;
#define INF 0xFFFFFF
// 暴力法
int baoli(int n,int e)
{
	// 只有一个鸡蛋，考虑最好情况从低到高依次遍历
	if(e == 1)
		return n;
	// 楼层只有0或1层就返回
	if(n == 0 || n == 1)
		return n;
	//
	int mint = INF;
	for(int i=1;i<=n;i++)
	{
		mint = min(mint, max(baoli(i-1, e-1), baoli(n-i, e)) + 1);
	}
	return mint;
}
// 二维数组dp
int dp_2(int n, int e)
{
	//
	int **dp = new int*[n+1];
	for(int i=0;i<=n;i++)
		dp[i] = new int[e+1];
	
	// 只有一个鸡蛋
	for(int i=0;i<=n;i++)
	{
		dp[i][1] = i;
	}
	//楼层为0或1
	for(int i=0;i<=e;i++)
	{
		dp[0][i] = 0;
		dp[1][i] = 1;	
	}
	//
	for(int i=2;i<=n;i++)
	{
		for(int j=2;j<=e;j++)
		{
			dp[i][j] = INF;
			// 遍历每一楼层
			for(int k=1;k<=i;k++)
			{
				dp[i][j] = min(dp[i][j], max(dp[k-1][j-1], dp[i-k][j]) + 1);
			}
		}
	}
	return dp[n][e];
}
// 一维数组
int dp_1(int n,int e)
{
	int a1[n+1],a2[n+1];
	// 初始化鸡蛋个数为1
	for(int i=0;i<=n;i++)
	{
		a1[i] = i;
		a2[i] = i;
	}
	//
	for(int j=2;j<=e;j++)
	{
		for(int i=2;i<=n;i++)
		{
			a2[i] = INF;
			for(int k=1;k<=i;k++)
			{
				a2[i] = min(a2[i], max(a1[k-1], a2[i-k])+1);
			}
		}
		// 调整数组
		for(int i=0;i<=n;i++)
		{
			a1[i] = a2[i];
		}
	}
	return a2[n];
}
// 逆向思维
int reverse(int n, int k) {
    int dp[k+1];
    for(int i=0;i<=k;i++)
        dp[i] = 0;
    int m = 0;
    while (dp[k] < n)
    {
        m++;
        for (int i = k; i >= 1; i--)
        	dp[i] = dp[i] + dp[i - 1] + 1;
    }
    return m;
}
// 二分查找
int erfen(int n, int e)
{
	int dp[n+1][e+1];
	// 只有一个鸡蛋
	for(int i=0;i<=n;i++)
	{
		dp[i][1] = i;
	}
	//楼层为0或1
	for(int i=0;i<=e;i++)
	{
		dp[0][i] = 0;
		dp[1][i] = 1;	
	}
	// 
	for(int i=2;i<=n;i++)
	{
		for(int j=2;j<=e;j++)
		{
			dp[i][j] = INF;
			// 二分剪枝放鸡蛋
			int left = 1,right = i;
			while(left < right)
			{
				int mid = (left + right + 1) / 2;
				int br = dp[mid-1][j-1];	// 鸡蛋破碎
				int nbr = dp[i-mid][j];		// 鸡蛋没碎
				if(br > nbr)
				{
					right = mid - 1;
				}
				else
				{
					left = mid;
				}
			}
			dp[i][j] = max(dp[left-1][j-1], dp[i-left][j]) + 1;
		}
	}
	return dp[n][e];
}

clock_t startTime, endTime;//秒级程序计时
int main()
{
	// 输入楼层高度、鸡蛋总数 
	cout<<"请输入楼层高度N，鸡蛋总数E\n";
	int N,E;
	cin>>N>>E;
	//startTime = clock();
	auto start = std::chrono::high_resolution_clock::now();
    //cout<<baoli(N,E)<<endl;
	//cout<<dp_2(N,E)<<endl;	
	//cout<<dp_1(N,E)<<endl;
	//cout<<erfen(N,E)<<endl;
    cout<<reverse(N,E)<<endl;
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << duration.count() << " 微秒" << std::endl;
	//endTime = clock();
	//cout<<(double)(endTime - startTime)<<"ms\n";
	
	return 0;
}