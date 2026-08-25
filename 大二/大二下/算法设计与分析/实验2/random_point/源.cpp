#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <string>
#include <random>
#include <algorithm>
#include <iomanip>
using namespace std;
int main() {
    // 创建随机数生成器
    std::random_device rd;
    std::mt19937 generator(rd());
    int e = 1000;
        
    // 生成并写入随机数
    for (int j = 1; j <= 10; j++)
    {
        std::uniform_int_distribution<int>distribution(0, e * j - 1);
        std::string path = "random_point_xs" + to_string(e * j) + ".txt";
        //std::string path = std::to_string(j) + "00tw " + std::to_string(k) + ".txt";
        std::ofstream file(path);

        file << e * j << endl;
        file << (e * j) << endl;

        if (file.is_open()) {
            for (int i = 0; i < (e * j); i++)
            {
                double ra = distribution(generator), rb = distribution(generator);
                file << ra << " " << rb << endl;
            }            
            file.close();
            std::cout << "随机数已成功写入文件." << std::endl;
        }
        else {
            std::cerr << "无法打开文件." << std::endl;
        }
    }
    return 0;
}