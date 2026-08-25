#include<sstream>
#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_set>
#include <random>
using namespace std;
// 定义边的hash函数和比较函数
struct edge_hash {
    size_t operator()(const std::pair<int, int>& edge) const {
        int a = (edge.second > edge.first) ? edge.first : edge.second;
        int b = (edge.first < edge.second) ? edge.first : edge.second;
        return b * 111 + a;
    }
};

struct edge_cmp {
    bool operator()(const std::pair<int, int>& e1, const std::pair<int, int>& e2) const {
        return e1.first == e2.first && e1.second == e2.second;
    }
};

int main() {
    // 设置随机数种子
    std::random_device rd;
    std::mt19937 gen(rd());

    for (int n = 20; n < 100; n += 10)
    {
        int m = n*n; // 边数
        //std::uniform_int_distribution<int> dis(0, 100);

        // 生成图
        // 输出图信息到文件
        //string path = "p" + std::to_string(n) + "e" + std::to_string(m) + ".txt";
        string path = "p" + to_string(n) + ".txt";
        std::ofstream file(path);
        file << n << std::endl;
        //file << m << std::endl;

        int i = 0;
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
                //				//设置随机数种子
                //				srand((unsigned)time(NULL));
                //				int f = rand() % 100 + 1;
                                // edges.push_back(Edge1(i, j, f));
                file << i << " " << j << " " << f << std::endl;
            }
        }
        
        file.close();
        std::cout << "文件：" + path + "已经写入" << std::endl;
    }
    return 0;
}