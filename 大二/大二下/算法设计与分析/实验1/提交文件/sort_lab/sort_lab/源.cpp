#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <string>
#include <thread>
#include <algorithm>
#include <random>
using namespace std;

// 冒泡排序，从小到大
void bubbleSort(std::vector<int>& arr) {
    int n = arr.size();
    int i, j;
    for (i = 0; i < n - 1; ++i) {
        for (j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);             
            }
        }
    }
}

// 选择排序，从小到大
void selectSort(vector<int> &arr)
{
    int n = arr.size();
    for (int i = 0; i < n - 2; ++i) 
    {
        int k = i;
        for (int j = i + 1; j < n - 1; j++)
        {
            // 寻找最小的数据
            if (arr[k] > arr[j])
            {
                k = j;
            }
        }
        //如果当前不是最小就交换
        if (k != i)
        {
            swap(arr[k], arr[i]);
        }
    }
}

// 快速排序，从小到大
void Qsort(vector<int>& arr, int low, int high) {
    if (high <= low) return;
    int i = low;
    int j = high;
    int key = arr[low];
    while (true)
    {
        //从左向右找比key大的值
        while (arr[i] <= key)
        {
            i++;
            if (i == high) 
            {
                break;
            }
        }
        //从右向左找比key小的值
        while (arr[j] >= key)
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
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    //中枢值与j对应值交换
    arr[low] = arr[j];
    arr[j] = key;
    Qsort(arr, low, j - 1);
    Qsort(arr, j + 1, high);
}

// 插入排序，从小到大
void insert_Sort(vector<int>& arr)
{
    int n = arr.size();
    for (int i = 0; i < n - 1; i++)
    {
        // 取出待插入的数据
        int temp = arr[i];
        // 往前面插入
        for (int j = i - 1; j >= 0; j--)
        {
            // 从小到大排序
            if (arr[j] > temp)
            {
                arr[j + 1] = arr[j];
            }
            else
            {
                //小于等于就插入到后一个位置
                arr[j + 1] = temp;
                break;
            }
        }
    }
}

// 归并排序，从小到大
void merge_Sort(vector<int>& arr)
{
    int n = arr.size();
    int deta = 2;
    while (deta < n)
    {
        for (int i = 0; i + deta <= n; i += deta)
        {
            //对部分数据进行插入排序
            for (int k = i; k < i+deta; k++)
            {
                // 取出待插入的数据
                int temp = arr[k];
                // 往前面插入
                for (int j = k - 1; j >= 0; j--)
                {
                    // 从小到大排序
                    if (arr[j] > temp)
                    {
                        arr[j + 1] = arr[j];
                    }
                    else
                    {
                        //小于等于就插入到后一个位置
                        arr[j + 1] = temp;
                        break;
                    }
                }
            }
            
        }
        //deta控制每次归并的数组大小
        deta = deta << 1;
    }
    //对全部再进行一次排序，保证准确性
    insert_Sort(arr);
}

// 合并两个有序数组
void merge(std::vector<int>& arr, int left, int mid, int right) {
    int n1 = mid - left + 1;    // 左侧数组的大小
    int n2 = right - mid;       // 右侧数组的大小

    // 创建临时数组
    std::vector<int> temp1(n1);
    std::vector<int> temp2(n2);

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
        if (temp1[i] <= temp2[j]) {
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

// 归并排序主函数
void mergeSort(std::vector<int>& arr, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSort(arr, left, mid);        // 对左侧数组进行排序
        mergeSort(arr, mid + 1, right);   // 对右侧数组进行排序
        merge(arr, left, mid, right);     // 合并两个有序数组
    }
}

string filename[3] = {"kuaisu","xuanze","duitiaozheng"};
// top_k问题
// 选择排序，从小到大
void k_selectSort(vector<int>& arr, int tk)
{
    int n = arr.size();
    for (int i = 0; i < tk; ++i)
    {
        int k = i;
        for (int j = i + 1; j < n - 1; j++)
        {
            // 寻找最小的数据
            if (arr[k] > arr[j])
            {
                k = j;
            }
        }
        //如果当前不是最小就交换
        if (k != i)
        {
            swap(arr[k], arr[i]);
        }
    }
}

// 调整最小堆
void minHeapify(std::vector<int>& arr, int n, int i) {
    int smallest = i;      // 根节点
    int left = 2 * i + 1;  // 左子节点
    int right = 2 * i + 2; // 右子节点

    // 如果左子节点小于根节点
    if (left < n && arr[left] < arr[smallest]) {
        smallest = left;
    }

    // 如果右子节点小于最小值
    if (right < n && arr[right] < arr[smallest]) {
        smallest = right;
    }

    // 如果最小值不是根节点，则交换节点并递归调整
    if (smallest != i) {
        std::swap(arr[i], arr[smallest]);
        minHeapify(arr, n, smallest);
    }
}

// 堆排序
void heapSort(std::vector<int>& arr, int tk) {
    int n = arr.size();

    // 构建最小堆
    for (int i = n / 2 - 1; i >= 0; i--) {
        minHeapify(arr, n, i);
    }

    // 逐个将最小元素移动到末尾
    for (int i = n - 1; i >= n - tk; i--) {
        std::swap(arr[0], arr[i]);
        minHeapify(arr, i, 0);
    }
}

int main() 
{
    /*
    for (int tk = 0; tk < 2; tk++)
    {
        //写入排序时间
        string file = "sort_time_" + filename[tk] + ".txt";
        ofstream sort_time(file);

        for (int i = 1; i <= 5; i++)
        {
            sort_time << to_string(i) + "00万规模：\n";

            for (int j = 1; j <= 20; j++)
            {
                string path = "D:/作业/算法设计与分析/实验1/random_num/random_num/" + to_string(i) + "00tw " + to_string(j) + ".txt";
                // 从文件中读取数据
                ifstream file(path);
                if (!file.is_open()) {
                    cerr << "无法打开文件." << endl;
                    return 1;
                }
                else
                {
                    cout << "成功打开文件" << path << endl;
                }

                vector<int> data;
                int num;
                while (file >> num) {
                    data.push_back(num);
                }
                file.close();


                random_device rd;
                mt19937 g(rd());
                shuffle(data.begin(), data.end(), g);

                // 排序并计时
                auto start = chrono::steady_clock::now();

                //mergeSort(data, 0, data.size() - 1);

                if (tk == 0)
                {
                    Qsort(data, 0, data.size() - 1);    //快速排序  
                }
                else if (tk == 1)
                {
                    //insert_Sort(data);      //插入排序
                    mergeSort(data, 0, data.size() - 1);    //归并排序
                }       

                auto end = chrono::steady_clock::now();
                auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);

                // 输出排序时间
                sort_time << duration.count() << endl;

                cout << to_string(i) + "00w 规模第" + to_string(j) + "次" << endl;
                cout << "排序时间： " << duration.count() << " ms" << endl;

                // 休眠10秒钟
                //std::this_thread::sleep_for(std::chrono::seconds(5));
            }
        }
        
    }*/

        //写入排序时间
        string file = "sort_time_topk_qsort.txt";
        ofstream sort_time(file);
        for (int i = 1; i <= 1000; i *= 10)
        {
            sort_time << to_string(i) + "万规模：\n";

            for (int j = 1; j <= 20; j++)
            {
                string path = "D:/作业/算法设计与分析/实验1/random_num/random_num/Top_K_" + to_string(i) + "tw " + to_string(j) + ".txt";
                // 从文件中读取数据
                ifstream file(path);
                if (!file.is_open()) {
                    cerr << "无法打开文件." << endl;
                    return 1;
                }
                else
                {
                    cout << "成功打开文件" << path << endl;
                }

                vector<int> data;
                int num;
                while (file >> num) {
                    data.push_back(num);
                }
                file.close();


                random_device rd;
                mt19937 g(rd());
                shuffle(data.begin(), data.end(), g);

                // 排序并计时
                auto start = chrono::steady_clock::now();

                //mergeSort(data, 0, data.size() - 1);

                //insert_Sort(data);      //插入排序
                //k_selectSort(data, tk);
                //heapSort(data, tk);         
                Qsort(data, 0, data.size() - 1);

                auto end = chrono::steady_clock::now();
                auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);

                // 输出排序时间
                sort_time << duration.count() << endl;

                cout << to_string(i) + "w 规模第" + to_string(j) + "次" << endl;
                cout << "排序时间： " << duration.count() << " ms" << endl;

                // 休眠10秒钟
                //std::this_thread::sleep_for(std::chrono::seconds(5));
            }
        }
    /*
    //test
    vector<int>arr;
    for (int i = 0; i < 12; i++)
    {
        int t;
        cin >> t;
        arr.push_back(t);
    }
    insert_Sort(arr);
    for (int i = 0; i < arr.size(); i++)
    {
        cout << arr[i] << " ";
    }
    cout << endl;
    */
    return 0;
}