#include <iostream>
#include <vector>
#include <random>
#include <ctime>
#include <chrono>
#define KB 1024
using namespace std;
// 数组的大小
vector<int> sizes{ 8,16,32,64,128,256,384,512,768,1024,1536,2048,3072,4096,5120,6144,7168,8192,10240,12288,16384,21504,27648};
// 随机种子
random_device rd;
mt19937 gen(rd());
void test(int size)
{
	// 开辟对应大小空间的数组
	int n = size / (sizeof(int));
	int *arr = new int[n];
	// 数组初始化，进行缓存预热
	memset(arr, 1, sizeof(int)*n);		
	std::uniform_int_distribution<> num(0, n-1);
	// 随机对数组访问1e8次
	// 记录开始访问时间
	auto start = std::chrono::high_resolution_clock::now();
	int sum = 0;
	for(int i=0;i < 1e8;i++)
	{
		sum += arr[num(gen)];
	}
	// 输出访问总时间
	auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout <<"Size:"<<(size/1024)<<"KB  Time："<< (duration.count()/1e6) << "s" << endl;
	delete []arr;
}
int MaxStride = 2048;

void CacheLine(int stride)
{
	// 开辟一个大小大于L1 Cache的数组
	int size = 1e9;
	int n = size/(sizeof(char));
	char *arr = new char[n];
	int sum = 0;
	// 记录开始访问时间
	auto start = std::chrono::high_resolution_clock::now();
	for(int i=0;i<=stride;i++)
	{
		for(int j=0;j<n;j+=stride)
		{
			sum+=arr[j];
		}
	}
	// 输出访问总时间
	auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout <<"stride:"<<stride<<"KB  Time："<< (duration.count()/1e6) << "s" << endl;
	delete []arr;
}
int main()
{
	cout<<"Size(KB), Time(s)\n";
//	for(auto size:sizes)
//	{
//		test(size*1024);
//	}
	for(int i=1;i<=MaxStride;i*=2)
	{
		CacheLine(i);
	}
	return 0;
}