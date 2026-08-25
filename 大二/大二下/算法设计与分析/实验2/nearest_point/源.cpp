#include <iostream>
#include <istream>
#include <fstream>
#include <sstream>
#include <vector>
#include <chrono>
#include <string>
#include <thread>
#include <math.h>
using namespace std;
struct point
{
    double x;
    double y;
};
// 写入距离

void distance(vector<point>&arr)
{
    int n = arr.size();
    double min = 0;
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            point pa = arr[i], pb = arr[j];
            double dis = (pa.x - pb.x) * (pa.x - pb.x) + (pa.y - pb.y) * (pa.y - pb.y);
            dis = sqrt(dis);
            // 写入
            //dist << pa.x << " " << pa.y << "and" << pb.x << " " << pb.y << " dis:" << dis << endl;
            if (min > dis)
            {
                min = dis;
            }
        }
    }
    cout << "min:" << min << endl;
}
int main()
{
    // 写入查找时间
    string file = "find_time_baoli.txt";
    ofstream find_time(file);
    // 写入距离
    string disfile = "dis.txt";
    ofstream dis(disfile);
    for (int i = 1; i <= 1; i++)
    {
        for (int j = 1; j <= 1; j++)
        {
            string path = "D:/作业/算法设计与分析/实验2/random_point/random_point" + to_string(i) + "0w " + to_string(j) + ".txt";
            // 从文件中读取数据
            ifstream file(path);
            if (!file.is_open())
            {
                cerr << "无法打开文件" << endl;
                return 1;
            }
            else
            {
                cout << "成功打开文件" << path << endl;
            }
            // 读取点的数据
            vector<point>point_set;
            std::string line;
            while (std::getline(file, line)) { // 逐行读取文件  
                std::istringstream iss(line); // 使用字符串流处理每一行  
                double pa,pb;
                iss >> pa; iss >> pb;
                point t = { pa,pb };
                point_set.push_back(t);                
            }
            distance(point_set);
            //
        }
    }
    return 0;
}