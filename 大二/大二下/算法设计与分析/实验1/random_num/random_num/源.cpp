#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <string>
#include <random>
#include <algorithm>
using namespace std;
int main() {
    // 创建随机数生成器
    std::random_device rd;
    std::mt19937 generator(rd());
    std::uniform_int_distribution<int> distribution(1, 100000000);

    
    // 生成并写入随机数
    for (int j = 1; j <= 1000; j *= 10)
    {
        for (int k = 1; k <= 20; k++)
        {
            std::string path = "Top_K_" + std::to_string(j) + "tw " + std::to_string(k) + ".txt";
            //std::string path = std::to_string(j) + "00tw " + std::to_string(k) + ".txt";
            std::ofstream file(path);
            if (file.is_open()) {
                for (int i = 0; i < 10000*j; ++i) {
                    int random_number = distribution(generator);
                    file << random_number << "\n";
                }
                file.close();
                std::cout << "随机数已成功写入文件." << std::endl;
            }
            else {
                std::cerr << "无法打开文件." << std::endl;
            }
        }
    }
    return 0;
}