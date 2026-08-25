#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <sstream>
#include <string>
#include <thread>
#include <algorithm>
#include <random>
using namespace std;
#define INF 0XFFFFFF;
struct point
{
    double x;
    double y;
};

// 暴力法计算
void distance(vector<point>& arr)
{
    int n = arr.size();
    double min = INF;
    point a, b;
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = i + 1; j < n; j++)
        {	// 计算两点的距离
            point pa = arr[i], pb = arr[j];
            double dis = (pa.x - pb.x) * (pa.x - pb.x) + (pa.y - pb.y) * (pa.y - pb.y);
            dis = sqrt(dis);
            if (min > dis)
            {	// 更新最小距离
                min = dis;
                a = arr[i];
                b = arr[j];
            }
        }
    }
    cout << "min:" << min << "(" << a.x << "," << a.y << ") (" << b.x << "," << b.y << ")" << endl;
}


// 按照x坐标升序
bool com(point& a, point& b)
{
    return a.x < b.x;
}

// 计算两点的距离
double dist(point pa, point pb)
{
    double dis = (pa.x - pb.x) * (pa.x - pb.x) + (pa.y - pb.y) * (pa.y - pb.y);
    dis = sqrt(dis);
    return dis;
}

// 快速排序，从小到大
void Qsort(vector<point>& arr, int low, int high) {
    if (high <= low) return;
    int i = low;
    int j = high;
    point key = arr[low];
    while (true)
    {
        //从左向右找比key大的值
        while (arr[i].y <= key.y)
        {
            i++;
            if (i == high)
            {
                break;
            }
        }
        //从右向左找比key小的值
        while (arr[j].y >= key.y)
        {
            j--;
            if (j == low)
            {
                break;
            }
        }
        //如果low指针小于high指针则结束排序
        if (i >= j)
            break;

        //交换i,j对应的值，继续满足 左小右大
        point temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    //中枢值与j对应值交换
    arr[low] = arr[j];
    arr[j] = key;
    Qsort(arr, low, j - 1);
    Qsort(arr, j + 1, high);
}

bool comp(point& a, point& b)
{
    return a.y < b.y;
}
// 合并两个有序数组
void merge_sort(std::vector<point>& arr, int left, int mid, int right) {
    int n1 = mid - left + 1;    // 左侧数组的大小
    int n2 = right - mid;       // 右侧数组的大小

    // 创建临时数组
    std::vector<point> temp1(n1);
    std::vector<point> temp2(n2);

    // 将数据复制到临时数组
    for (int i = 0; i < n1; i++) {
        temp1[i] = arr[left + i];
    }
    for (int j = 0; j < n2; j++) {
        temp2[j] = arr[mid + 1 + j];
    }

    // 归并临时数组的元素到原数组
    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (temp1[i].y <= temp2[j].y) {
            arr[k] = temp1[i];
            i++;
        }
        else {
            arr[k] = temp2[j];
            j++;
        }
        k++;
    }

    // 将剩余的元素复制到原数组
    while (i < n1) {
        arr[k] = temp1[i];
        i++;
        k++;
    }
    while (j < n2) {
        arr[k] = temp2[j];
        j++;
        k++;
    }
}

// 合并
double merge(vector<point>& arr, int low, int mid, int high, double mind)
{
    // 存入中线附近+-最短距离的点
    vector<point>temp;
    for (int i = low; i <= high; i++)
    {
        if (arr[i].x > arr[mid].x - mind && arr[i].x < arr[mid].x + mind)
        {
            point t = arr[i];
            temp.push_back(t);
        }
    }
    // 对区域内的点集按照y轴坐标排序
    //Qsort(temp, 0, temp.size()-1);	// 快速排序
    merge_sort(temp, 0, temp.size() >> 1, temp.size() - 1);	//归并排序
    // 求取最小点 
    for (int i = 0; i < temp.size(); i++)
    {
        for (int j = i + 1; j < temp.size() && j < i + 6; j++)
        {	// 纵坐标差大于mind则跳过
            if (temp[j].y - temp[i].y > mind)
                break;
            // 如果距离更小则更新最小值
            double t = dist(temp[i], temp[j]);
            if (mind > t)
                mind = t;
        }
    }
    return mind;
}
double fenzhi(vector<point>& arr, int low, int high)
{
    // 只有一个点
    if (low == high)
    {
        return INF;
    }
    // 只有两个点
    else if (low + 1 == high)
    {
        return dist(arr[low], arr[high]);
    }
    // 多个点则递归二分
    else
    {
        // 取出中间点二分
        int mid = (low + high) >> 1;
        double dl = fenzhi(arr, low, mid);
        double dr = fenzhi(arr, mid + 1, high);
        double mindist = dl < dr ? dl : dr;
        // 合并
        double t = merge(arr, low, mid, high, mindist);
        mindist = mindist < t ? mindist : t;
        //cout<<mindist<<endl;
        return mindist;
    }
}
int main()
{
    // 写入查找时间
    string file = "find_time_baoli.txt";
    ofstream find_time(file);
    for (int i = 7; i <= 10; i++)
    {
        find_time << to_string(i) + "0w规模\n";
        for (int j = 1; j <= 10; j++)
        {
            string path = "D:/data/random_point" + to_string(i) + "0w " + to_string(j) + ".txt";
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
                double pa, pb;
                iss >> pa; iss >> pb;
                point t = { pa,pb };
                point_set.push_back(t);
            }
            // 排序并计时
            auto start = chrono::steady_clock::now();

            //distance(point_set);		//暴力法
            //分治法
            sort(point_set.begin(), point_set.end(), com);
            fenzhi(point_set, 0, point_set.size() - 1);

            auto end = chrono::steady_clock::now();
            auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);

            find_time << duration.count() << endl;
            cout << duration.count() << "ms\n";
            //
        }
    }
    return 0;
}